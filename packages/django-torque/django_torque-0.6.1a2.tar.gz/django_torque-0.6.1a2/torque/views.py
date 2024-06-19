import orjson
import json
import urllib.parse
from werkzeug.utils import secure_filename
from datetime import datetime
from django.core.files.base import ContentFile
from django.db.models import Q, F, Count
from django.http import HttpResponse, JsonResponse, FileResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from torque import models
from django.contrib.postgres.search import SearchQuery, SearchRank
from django.conf import settings
from torque import utils
from torque.version import __version__

import magic
import time
import csv

jinja_env = utils.get_jinja_env()


def get_wiki(dictionary, collection_name):
    wiki_key = dictionary["wiki_key"]

    if "wiki_keys" in dictionary:
        wiki_keys = dictionary["wiki_keys"].split(",")
        collection_names = dictionary["collection_names"].split(",")
        mapping = dict(zip(collection_names, wiki_keys))

        if collection_name in mapping:
            wiki_key = mapping[collection_name]

    return models.Wiki.objects.get_or_create(wiki_key=wiki_key)[0]


def get_wiki_from_request(request, collection_name):
    return get_wiki(request.GET, collection_name)


def get_system_information(request, fmt):
    if fmt == "json":
        information = {}
        if getattr(settings, "TORQUE_COLLECTIONS_ALIAS", False) and getattr(
            settings, "TORQUE_DOCUMENTS_ALIAS", False
        ):
            information["collections_alias"] = settings.TORQUE_COLLECTIONS_ALIAS
            information["documents_alias"] = settings.TORQUE_DOCUMENTS_ALIAS

        information["server_version"] = __version__
        return JsonResponse(
            information,
            safe=False,
        )
    else:
        raise Exception(f"Invalid format {fmt}")


memory_cache = {}


def create_counts(results_filtered_data, filters):
    torque_filters_by_name = {
        f.name(): f for f in getattr(settings, "TORQUE_FILTERS", [])
    }
    compiled_filter_results = {
        filter.name(): {
            value: {"name": value, "total": 0}
            for value in filters.get(filter.name(), [])
        }
        for filter in getattr(settings, "TORQUE_FILTERS", [])
    }
    for result_filtered_data in results_filtered_data:
        for filter in getattr(settings, "TORQUE_FILTERS", []):
            selected = True

            for name, values in filters.items():
                if name != filter.name() and values:
                    filter_passed = False
                    for value in values:
                        if name in result_filtered_data.keys():
                            if (
                                torque_filters_by_name[name].is_list()
                                and value in result_filtered_data[name]
                            ):
                                filter_passed = True
                                break
                            elif (
                                not torque_filters_by_name[name].is_list()
                                and value == result_filtered_data[name]
                            ):
                                filter_passed = True
                                break
                    if not filter_passed:
                        selected = False

            if selected:
                counts = compiled_filter_results[filter.name()]
                if filter.name() in result_filtered_data:
                    if filter.is_list():
                        for value in result_filtered_data[filter.name()]:
                            if value not in filter.ignored_values():
                                if value not in counts:
                                    counts[value] = {"name": value, "total": 0}

                                counts[value]["total"] += 1
                    else:
                        value = result_filtered_data[filter.name()]
                        if value not in filter.ignored_values():
                            if value not in counts:
                                counts[value] = {"name": value, "total": 0}

                            counts[value]["total"] += 1
    return compiled_filter_results


def original(results_filtered_data, filters):
    filter_results = []
    torque_filters_by_name = {
        f.name(): f for f in getattr(settings, "TORQUE_FILTERS", [])
    }
    for filter in getattr(settings, "TORQUE_FILTERS", []):
        thread_start = time.perf_counter()
        selected_objects = []

        def result_filtered_data_addable(result_filtered_data):
            for name, values in filters.items():
                if name != filter.name() and values:
                    filter_passed = False
                    for value in values:
                        if name in result_filtered_data.keys():
                            if (
                                torque_filters_by_name[name].is_list()
                                and value in result_filtered_data[name]
                            ):
                                filter_passed = True
                                break
                            elif (
                                not torque_filters_by_name[name].is_list()
                                and value == result_filtered_data[name]
                            ):
                                filter_passed = True
                                break
                    if not filter_passed:
                        return False
            return True

        selected_objects = [
            result_filtered_data
            for result_filtered_data in results_filtered_data
            if result_filtered_data_addable(result_filtered_data)
        ]

        counts = {}
        for selected_object in selected_objects:
            if filter.name() in selected_object:
                if filter.is_list():
                    for value in selected_object[filter.name()]:
                        if value not in filter.ignored_values():
                            if value not in counts:
                                counts[value] = {"name": value, "total": 0}

                            counts[value]["total"] += 1
                else:
                    value = selected_object[filter.name()]
                    if value not in filter.ignored_values():
                        if value not in counts:
                            counts[value] = {"name": value, "total": 0}

                        counts[value]["total"] += 1

        for value in filters.get(filter.name(), []):
            if value not in counts:
                counts[value] = {"name": value, "total": 0}

        filter_result = {
            "name": filter.name(),
            "display": filter.display_name(),
            "counts": {name: counts[name] for name in filter.sort(list(counts.keys()))},
        }

        filter_results.append(filter_result)

    return filter_results


# With ProcessPool Executor
def attempt_5(results_filtered_data, filters):
    from concurrent.futures import ProcessPoolExecutor

    with ProcessPoolExecutor(8) as executor:
        last = time.perf_counter()
        all_compiled_results = list(
            executor.map(
                create_counts,
                [results_filtered_data[i::8] for i in range(8)],
                [filters for i in range(8)],
            )
        )

        print("Attmpt 5-1: " + str(time.perf_counter() - last))
        last = time.perf_counter()
        all_compiled_results = list(
            executor.map(
                create_counts,
                [results_filtered_data[i::8] for i in range(8)],
                [filters for i in range(8)],
            )
        )
        print("Attmpt 5-1: " + str(time.perf_counter() - last))
        last = time.perf_counter()
        all_compiled_results = [
            create_counts(results_filtered_data[i::8], filters) for i in range(8)
        ]
        print("Attmpt 5-2: " + str(time.perf_counter() - last))

    filter_results = []

    for filter in getattr(settings, "TORQUE_FILTERS", []):
        counts = {}
        for compiled_results in all_compiled_results:
            for compiled_count in compiled_results[filter.name()].values():
                name = compiled_count["name"]
                if name not in counts:
                    counts[name] = {"name": name, "total": 0}
                counts[name]["total"] += compiled_count["total"]

        filter_results.append(
            {
                "name": filter.name(),
                "display": filter.display_name(),
                "counts": {
                    name: counts[name] for name in filter.sort(list(counts.keys()))
                },
            }
        )

    return filter_results


count_cache = {}


# Memory Cache
def attempt_6(ids, filters):
    start = time.perf_counter()

    for id in ids:
        rfd = memory_cache[id]
        if id not in count_cache:
            count_cache_object = {"base": {}, "composed": {}}
            for target_filter in getattr(settings, "TORQUE_FILTERS", []):
                target_values = rfd.get(target_filter.name(), [])
                if not target_filter.is_list() and target_values:
                    target_values = [target_values]

                count_cache_object["base"][target_filter.name()] = target_values
                count_cache_object["composed"][target_filter.name()] = {}

                for target_value in target_values:
                    count_cache_object["composed"][target_filter.name()][
                        target_value
                    ] = True
            #                    for source_filter in getattr(settings, "TORQUE_FILTERS", []):
            #                        source_values = rfd.get(source_filter.name(), [])
            #                        if not source_filter.is_list() and source_values:
            #                            source_values = [source_values]
            #
            #                        for source_value in source_values:
            #                            count_cache_object["composed"][target_filter.name()][target_value][source_filter.name()] = True
            count_cache[id] = count_cache_object
    #            print(count_cache_object["composed"]["competition_name"])
    #            break

    print("Building the cache: " + str(time.perf_counter() - start))
    start = time.perf_counter()

    filter_results = []

    building_1 = 0
    building_2 = 0
    for source_filter in getattr(settings, "TORQUE_FILTERS", []):
        counts = {
            value: {"name": value, "total": 0}
            for value in filters.get(source_filter.name(), [])
        }
        for id in ids:
            start = time.perf_counter()
            potential_counts = {
                value: 0 for value in count_cache[id]["base"][source_filter.name()]
            }
            num_applicable_filters = 0
            for target_filter_name, target_filter_values in filters.items():
                if target_filter_name != source_filter.name():
                    num_applicable_filters += 1
                    for target_filter_value in target_filter_values:
                        if count_cache[id]["composed"][target_filter_name].get(
                            target_filter_value
                        ):
                            for value in count_cache[id]["base"][source_filter.name()]:
                                potential_counts[value] += 1
                            break  # If you match multiple target values, still only increment by 1
            building_1 += time.perf_counter() - start

            start = time.perf_counter()
            for potential_count, num in potential_counts.items():
                if num == num_applicable_filters:
                    if potential_count not in counts:
                        counts[potential_count] = {"name": potential_count, "total": 0}
                    counts[potential_count]["total"] += 1
            building_2 += time.perf_counter() - start

        filter_results.append(
            {
                "name": source_filter.name(),
                "display": source_filter.display_name(),
                "counts": {
                    name: counts[name]
                    for name in source_filter.sort(list(counts.keys()))
                },
            }
        )

    print("Building 1: " + str(building_1))
    print("Building 2: " + str(building_2))

    print("Using the cache: " + str(time.perf_counter() - start))
    return filter_results


def attempt_7(ids, filters):
    cache_build_start = time.perf_counter()
    for id in ids:
        rfd = memory_cache[id]
        if id not in count_cache:
            count_cache_object = {}
            for target_filter in getattr(settings, "TORQUE_FILTERS", []):
                target_values = rfd.get(target_filter.name(), [])
                if not target_filter.is_list() and target_values:
                    target_values = [target_values]

                count_cache_object[target_filter.name()] = {}

                for target_value in target_values:
                    count_cache_object[target_filter.name()][target_value] = True
            count_cache[id] = count_cache_object

    filter_results = []
    torque_filters_by_name = {
        f.name(): f for f in getattr(settings, "TORQUE_FILTERS", [])
    }
    print("Cache Build: " + str(time.perf_counter() - cache_build_start))
    building_1 = 0
    building_2 = 0

    def result_filtered_data_addable(id, filters):
        for name, values in filters.items():
            if values:
                filter_passed = False
                for value in values:
                    try:
                        if count_cache[id][name][value]:
                            filter_passed = True
                            break
                    except KeyError:
                        count_cache[id][name][value] = False

                if not filter_passed:
                    return False
        return True

    efl_start = time.perf_counter()
    empty_filter_list = [
        memory_cache[id] for id in ids if result_filtered_data_addable(id, filters)
    ]
    print("Empty Filter List: " + str(time.perf_counter() - efl_start))

    for filter in getattr(settings, "TORQUE_FILTERS", []):
        thread_start = time.perf_counter()

        filters_we_care_about = {
            name: values for name, values in filters.items() if name != filter.name()
        }

        start = time.perf_counter()
        if filter.name() not in filters or not filters[filter.name()]:
            selected_objects = empty_filter_list
        else:
            selected_objects = [
                memory_cache[id]
                for id in ids
                if result_filtered_data_addable(id, filters_we_care_about)
            ]

        building_1 += time.perf_counter() - start

        start = time.perf_counter()
        counts = {}
        for selected_object in selected_objects:
            if filter.name() in selected_object:
                if filter.is_list():
                    for value in selected_object[filter.name()]:
                        if value not in filter.ignored_values():
                            if value not in counts:
                                counts[value] = {"name": value, "total": 0}

                            counts[value]["total"] += 1
                else:
                    value = selected_object[filter.name()]
                    if value not in filter.ignored_values():
                        if value not in counts:
                            counts[value] = {"name": value, "total": 0}

                        counts[value]["total"] += 1

        for value in filters.get(filter.name(), []):
            if value not in counts:
                counts[value] = {"name": value, "total": 0}
        building_2 += time.perf_counter() - start

        filter_result = {
            "name": filter.name(),
            "display": filter.display_name(),
            "counts": {name: counts[name] for name in filter.sort(list(counts.keys()))},
        }

        filter_results.append(filter_result)

    print("Building 1: " + str(building_1))
    print("Building 2: " + str(building_2))

    return (filter_results, len(empty_filter_list))


def search_data(
    qs, filters, wiki_configs, documents_limited_to, omit_filter_results=False
):

    print("******************")
    start = time.perf_counter()
    data_vector_q = Q()
    if qs:
        for q in qs:
            data_vector_q |= Q(data_vector=q)

    print("A: " + str(time.perf_counter() - start))

    document_limit_or = Q()
    for collection, document in documents_limited_to:
        document_limit_or |= Q(collection__name=collection, document__key=document)
    print("B: " + str(time.perf_counter() - start))

    results = (
        models.SearchCacheDocument.objects.filter(
            data_vector_q,
            document_limit_or,
            collection__in=list(wiki_configs.values_list("collection", flat=True)),
            wiki__wiki_key__in=list(
                wiki_configs.values_list("wiki__wiki_key", flat=True)
            ),
            group__in=list(wiki_configs.values_list("group", flat=True)),
            wiki_config__id__in=list(wiki_configs.values_list("id", flat=True)),
        )
        .select_related("document")
        .select_related("collection")
    )
    torque_filters_by_name = {
        f.name(): f for f in getattr(settings, "TORQUE_FILTERS", [])
    }
    print("C: " + str(time.perf_counter() - start))
    if not omit_filter_results:
        all_ids = list(results.values_list("id", flat=True))
        cache_missed_ids = [id for id in all_ids if id not in memory_cache]
        print(len(cache_missed_ids))
        for result in models.SearchCacheDocument.objects.filter(
            id__in=cache_missed_ids
        ).values("id", "filtered_data"):
            memory_cache[result["id"]] = result["filtered_data"]
        results_filtered_data = [memory_cache[id] for id in all_ids]

        print("C1: " + str(time.perf_counter() - start))

        print("D: " + str(time.perf_counter() - start))
        # import threading
        # lock = threading.Lock()

        # filter_results = original(results_filtered_data, filters)
        # filter_results = attempt_5(results_filtered_data, filters)
        # filter_results = attempt_6(all_ids, filters)
        (filter_results, num_results) = attempt_7(all_ids, filters)
        print("E: " + str(time.perf_counter() - start))
    else:
        filter_results = None
        num_results = None

    additional_filters = []
    for name, values in filters.items():
        q_objects = Q()
        if torque_filters_by_name[name].is_list():
            key = "filtered_data__%s__contains" % name
        else:
            key = "filtered_data__%s" % name
        for value in values:
            q_dict = {key: value}
            q_objects |= Q(**q_dict)
        additional_filters.append(q_objects)
    print("F: " + str(time.perf_counter() - start))

    if qs:
        returned_results = (
            results.filter(*additional_filters)
            .annotate(rank=SearchRank(F("data_vector"), SearchQuery(q[0])))
            .order_by("-rank")
        )
    elif getattr(settings, "TORQUE_EXPLORE_RANK", None):
        returned_results = results.filter(*additional_filters).order_by("explore_rank")
    else:
        returned_results = results.filter(*additional_filters)
    print("G: " + str(time.perf_counter() - start))

    print("------------------")

    return (returned_results, filter_results, num_results)


def search(
    q, filters, offset, template_config, wiki_configs, documents_limited_to, fmt
):
    # search_data requires filter values to be lists
    filters = {name: [value] for (name, value) in filters.items()}

    (returned_results, filter_results, num_results) = search_data(
        [q], filters, wiki_configs, documents_limited_to
    )
    # While this result isn't actually mwiki text, this result is intended
    # for the mediawiki Torque extension.  Probably better to keep
    # the mwiki format than to do something like create a new "torque" format.
    # But, if we decide we need results to go to another renderer, it may
    # be worth being more clear about what we're doing here via the interface.
    #
    # This has gotten weird because the results are actually html from cached
    # results
    if fmt == "mwiki":
        template = models.Template.objects.get(
            type="Search",
            collection=template_config.collection,
            wiki=template_config.wiki,
        )

        cache_or = Q()
        for r in returned_results[offset : (offset + 20)]:
            cache_or |= Q(
                document_dict__wiki_config=r.wiki_config,
                document_dict__document=r.document,
            )

        mwiki_text = []

        if len(returned_results) != 0:
            cached_results = models.TemplateCacheDocument.objects.filter(
                template=template,
            ).filter(cache_or)

            for c in cached_results:
                if c.dirty or c.rendered_text == "":
                    mwiki_text.append({"text": c.to_mwiki(), "fmt": "mwiki"})
                else:
                    mwiki_text.append({"text": c.rendered_text, "fmt": "html"})

        return JsonResponse(
            {
                "num_results": returned_results.count(),
                "mwiki_text": json.dumps(mwiki_text),
                "filter_results": filter_results,
            },
            safe=False,
        )
    elif fmt == "json":
        response = [
            "/%s/%s/%s/%s"
            % (
                settings.TORQUE_COLLECTIONS_ALIAS or "collections",
                result.collection.name,
                settings.TORQUE_DOCUMENTS_ALIAS or "documents",
                result.document.key,
            )
            for result in returned_results
        ]

        return JsonResponse(response, safe=False)
    else:
        raise Exception(f"Invalid format {fmt}")


def search_global(request, fmt):
    q = request.GET["q"]
    f = json.loads(request.GET["f"]) if "f" in request.GET and request.GET["f"] else {}
    results_limit_json = json.loads(request.body) if request.body else None
    results_limit = results_limit_json if results_limit_json else []
    offset = int(request.GET.get("offset", 0))
    group = request.GET["group"]
    global_wiki_key = request.GET["wiki_key"]
    global_collection_name = request.GET["collection_name"]
    wiki_keys = request.GET["wiki_keys"].split(",")
    collection_names = request.GET["collection_names"].split(",")
    global_config = models.WikiConfig.objects.get(
        collection__name=global_collection_name,
        wiki__wiki_key=global_wiki_key,
        group=group,
    )
    configs = models.WikiConfig.objects.filter(
        collection__name__in=collection_names, wiki__wiki_key__in=wiki_keys, group=group
    ).all()
    return search(q, f, offset, global_config, configs, results_limit, fmt)


def search_collection(request, collection_name, fmt):
    q = request.GET["q"]
    f = json.loads(request.GET["f"]) if "f" in request.GET and request.GET["f"] else {}
    results_limit_json = json.loads(request.body) if request.body else None
    results_limit = (
        [[collection_name, key] for key in results_limit_json]
        if results_limit_json
        else []
    )
    offset = int(request.GET.get("offset", 0))
    group = request.GET["group"]
    wiki = get_wiki_from_request(request, collection_name)
    configs = models.WikiConfig.objects.filter(
        collection__name=collection_name, wiki=wiki, group=group
    )
    return search(q, f, offset, configs.first(), configs, results_limit, fmt)


result_cache = {}


def explore(
    qs,
    filters,
    offset,
    template_name,
    template_config,
    wiki_configs,
    results_limit,
    filters_only=False,
    with_ids=False,
):

    start = time.perf_counter()
    (returned_results, filter_results, num_results) = search_data(
        qs, filters, wiki_configs, results_limit, not filters_only
    )
    print("Search data taken: " + str(time.perf_counter() - start))
    # print(returned_results.count())
    # print("Num results data taken: " + str(time.perf_counter() - start))

    response = {
        "num_results": num_results,
        "filter_results": filter_results,
    }

    if not filters_only:
        mwiki_text = ""

        result_start = time.perf_counter()
        result_ids = list(
            returned_results[offset : (offset + 100)].values_list("id", flat=True)
        )
        cache_missed_ids = [id for id in result_ids if id not in result_cache]
        print(len(cache_missed_ids))
        for r in models.SearchCacheDocument.objects.filter(id__in=cache_missed_ids):
            result_cache[r.id] = {
                "collection_name": r.collection.name,
                "document_key": r.document.key,
                "fields": orjson.loads(
                    models.DocumentDictCache.objects.get(
                        document=r.document, wiki_config__group=r.group
                    ).dictionary
                )["fields"],
            }
        result_set = [result_cache[id] for id in result_ids]
        print("R1: " + str(time.perf_counter() - result_start))
        # result_set = list(returned_results[offset : (offset + 100)])
        # print("R2: " + str(time.perf_counter() - result_start))
        # result_set = [
        #    for r in result_set
        # ]
        # print("R3: " + str(time.perf_counter() - result_start))
        if not num_results:
            response["num_results"] = len(result_set)

        explore_templates = models.Template.objects.filter(
            type="Explore",
            collection=template_config.collection,
        )
        if explore_templates:
            if template_name:
                template = jinja_env.from_string(
                    explore_templates.get(name=template_name).get_file_contents()
                )
            else:
                template = jinja_env.from_string(
                    explore_templates.get(is_default=True).get_file_contents()
                )
            mwiki_text += template.render(
                {
                    template_config.collection.object_data_name(): [
                        r["fields"] for r in result_set
                    ]
                }
            )
        else:
            for result in result_set:
                template = jinja_env.from_string(
                    models.Template.objects.get(
                        name="Search", collection=template_config.collection
                    ).get_file_contents()
                )
                mwiki_text += (
                    "<div class='result'><div class='result--actions'><div class='result--select--holder' data-collection='%s' data-document='%s'></div></div>"
                    % (
                        result["collection_name"],
                        result["document_key"],
                    )
                )
                mwiki_text += template.render(
                    {template_config.collection.object_name: result["fields"]}
                )
                mwiki_text += "</div>"
                mwiki_text += "\n\n"

        if with_ids:
            response["results"] = [
                (r["collection__name"], r["document__key"])
                for r in returned_results.values("collection__name", "document__key")
            ]
        response["mwiki_text"] = mwiki_text
    print("All taken: " + str(time.perf_counter() - start))

    return JsonResponse(response, safe=False)


def explore_global(request):
    qs = (
        json.loads(request.GET["qs"])
        if "qs" in request.GET and request.GET["qs"]
        else []
    )
    f = json.loads(request.GET["f"]) if "f" in request.GET and request.GET["f"] else {}
    template_name = request.GET.get("template")
    results_limit_json = json.loads(request.body) if request.body else None
    results_limit = results_limit_json if results_limit_json else []
    offset = int(request.GET.get("offset", 0))
    group = request.GET["group"]
    global_wiki_key = request.GET["wiki_key"]
    global_collection_name = request.GET["collection_name"]
    filter_only = request.GET.get("filter_only", False)
    with_ids = request.GET.get("with_ids", False)
    wiki_keys = request.GET["wiki_keys"].split(",")
    collection_names = request.GET["collection_names"].split(",")
    global_config = models.WikiConfig.objects.get(
        collection__name=global_collection_name,
        wiki__wiki_key=global_wiki_key,
        group=group,
    )
    configs = models.WikiConfig.objects.filter(
        collection__name__in=collection_names, wiki__wiki_key__in=wiki_keys, group=group
    ).all()
    return explore(
        qs,
        f,
        offset,
        template_name,
        global_config,
        configs,
        results_limit,
        filter_only,
        with_ids,
    )


def explore_collection(request, collection_name):
    qs = (
        json.loads(request.GET["qs"])
        if "qs" in request.GET and request.GET["qs"]
        else []
    )
    results_limit_json = json.loads(request.body) if request.body else None
    results_limit = (
        [[collection_name, key] for key in results_limit_json]
        if results_limit_json
        else []
    )
    f = json.loads(request.GET["f"]) if "f" in request.GET and request.GET["f"] else {}
    template_name = request.GET.get("template")
    offset = int(request.GET.get("offset", 0))
    group = request.GET["group"]
    filter_only = request.GET.get("filter_only", False)
    with_ids = request.GET.get("with_ids", False)
    wiki = get_wiki_from_request(request, collection_name)
    configs = models.WikiConfig.objects.filter(
        collection__name=collection_name, wiki=wiki, group=group
    )
    return explore(
        qs,
        f,
        offset,
        template_name,
        configs.first(),
        configs,
        results_limit,
        filter_only,
        with_ids,
    )


def edit_record(collection_name, key, group, wiki, field, new_value):
    collection = models.Collection.objects.get(name=collection_name)
    document = models.Document.objects.get(collection=collection, key=key)
    wiki_config = models.WikiConfig.objects.get(
        collection=collection,
        wiki=wiki,
        group=group,
    )

    levels = field.split("||")

    if levels[0] in [field.name for field in wiki_config.valid_fields.all()]:
        value = document.values.get(field__name=levels[0])

        if len(levels) == 1:
            to_save = new_value
        else:
            to_save = value.to_python()

            inner_save = to_save
            for idx in range(1, len(levels)):
                level = levels[idx]
                if isinstance(inner_save, list):
                    level = int(level)

                if idx + 1 == len(levels):
                    inner_save[level] = new_value
                else:
                    inner_save = inner_save[level]

        value.latest = json.dumps(to_save)
        value.save()
        edit_record = models.ValueEdit(
            collection=collection,
            value=value,
            updated=json.dumps(to_save),
            message="",
            edit_timestamp=datetime.now,
            wiki=wiki,
        )
        edit_record.save()

    models.TableOfContentsCache.objects.filter(
        toc__in=collection.tables_of_contents.all()
    ).update(dirty=True)
    utils.dirty_documents([document])
    # Rebuild immediately because whoever is doing the editing probably
    # wants to see the fruits of their efforts.
    document.rebuild_cache(wiki_config)

    wiki.invalidate_linked_wiki_toc_cache()
    models.SearchCacheDocument.objects.filter(document=document).update(dirty=True)

    # This is overkill, but that's ok.  There's a bit of work to make it so
    # the individaul template cache documents have a dirty method
    collection.templates.update(dirty=True)

    collection.last_updated = datetime.now
    collection.save()


@csrf_exempt
@require_http_methods(["POST"])
def parse_for_edit(request):
    post_fields = json.loads(request.body)

    if getattr(settings, "TORQUE_EDIT_PROCESSOR", False):
        return JsonResponse(
            {"data": settings.TORQUE_EDIT_PROCESSOR(post_fields["data"])}
        )
    else:
        return JsonResponse({"data": post_fields["data"]})


def get_collections(request, fmt):
    collection_names = [x for x in request.GET["collection_names"].split(",") if x]

    return JsonResponse(collection_names, safe=False)


def get_collection(request, collection_name, fmt):
    if fmt == "json":
        response = {"name": collection_name}

        collection = models.Collection.objects.get(name=collection_name)

        if "group" in request.GET:
            group = request.GET["group"]
            wiki = get_wiki_from_request(request, collection_name)
            wiki_config = models.WikiConfig.objects.get(
                collection=collection,
                wiki=wiki,
                group=group,
            )

            response["fields"] = [
                field.name for field in wiki_config.valid_fields.all()
            ]
        elif "admin" in request.GET:
            response["fields"] = [field.name for field in collection.fields.all()]

        response["last_updated"] = collection.last_updated.isoformat()

        return JsonResponse(response)
    else:
        raise Exception(f"Invalid format {fmt}")


def get_toc(request, collection_name, toc_name, fmt):
    group = request.GET["group"]

    results_limit_json = json.loads(request.body) if request.body else None
    results_limit = results_limit_json if results_limit_json else []

    wiki = get_wiki_from_request(request, collection_name)
    collection = models.Collection.objects.get(name=collection_name)

    try:
        wiki_config = models.WikiConfig.objects.get(
            collection=collection,
            wiki=wiki,
            group=group,
        )
    except:
        return HttpResponse(status=403)

    toc = models.TableOfContents.objects.get(collection=collection, name=toc_name)

    if group == "":
        return HttpResponse(status=403)

    if fmt == "mwiki":
        return HttpResponse(toc.render_to_mwiki(wiki_config, results_limit))
    elif fmt == "html":
        if not results_limit:
            cached_toc = wiki_config.cached_tocs.get(toc=toc)
            if cached_toc.dirty:
                cached_toc.rebuild()
            return HttpResponse(cached_toc.rendered_html)
        else:
            return HttpResponse()
    else:
        raise Exception(f"Invalid format {fmt}")


def get_documents(request, collection_name, fmt):
    collection = models.Collection.objects.get(name=collection_name)
    group = request.GET.get("group")
    admin = request.GET.get("admin")
    wiki = get_wiki_from_request(request, collection_name)

    if fmt == "json":
        if group:
            wiki_config = models.WikiConfig.objects.get(
                collection=collection,
                wiki=wiki,
                group=group,
            )
            return JsonResponse(
                [document.key for document in wiki_config.valid_ids.all()], safe=False
            )
        elif admin:
            return JsonResponse(
                [document.key for document in collection.documents.all()], safe=False
            )
    else:
        raise Exception(f"Invalid format {fmt}")


def get_document(group, admin, wiki, key, version, fmt, collection_name, view=None):
    collection = models.Collection.objects.get(name=collection_name)

    wiki_config = None
    if group or not admin:
        wiki_config = models.WikiConfig.objects.get(
            collection=collection,
            wiki=wiki,
            group=group,
        )

        document = wiki_config.valid_ids.get(key=key, collection=collection).to_dict(
            wiki_config, version
        )["fields"]
    # We only allow admin style access to documents when using them from a data/api
    # point of view, just to be extra sure that normal wiki viewership remains group
    # based from both a permissions point of view, but also from a cache one
    elif admin and fmt in ["json", "dict"]:
        document = collection.documents.get(key=key).to_dict(None, version)["fields"]

    if fmt == "json":
        return JsonResponse(document)
    elif fmt == "dict":
        return document

    templates = models.Template.objects.filter(
        collection=collection,
        wiki=wiki,
        type="View",
    )

    if view is not None:
        try:
            view_object = json.loads(view)

            view_wiki = models.Wiki.objects.get(wiki_key=view_object["wiki_key"])
            view = view_object["view"]
            template = models.Template.objects.get(
                wiki=view_wiki, type="View", name=view
            )
        except json.JSONDecodeError:
            template = templates.get(name=view)
    else:
        template = templates.get(is_default=True)

    if fmt == "mwiki":
        rendered_template = jinja_env.from_string(template.get_file_contents()).render(
            {collection.object_name: document}
        )
        return HttpResponse(rendered_template)
    elif fmt == "html":
        try:
            ddc = models.DocumentDictCache.objects.get(
                wiki_config=wiki_config,
                document=wiki_config.valid_ids.get(key=key, collection=collection),
            )
            cache = models.TemplateCacheDocument.objects.get(
                template=template, document_dict=ddc
            )
            if cache.dirty:
                cache.rebuild()
            return HttpResponse(cache.rendered_text)
        except models.TemplateCacheDocument.DoesNotExist:
            return HttpResponse("")
    else:
        raise Exception(f"Invalid format {fmt}")


def get_document_view(request, collection_name, key, fmt, version="latest"):
    group = request.GET.get("group")
    admin = request.GET.get("admin")
    wiki = get_wiki_from_request(request, collection_name)

    return get_document(
        group,
        admin,
        wiki,
        key,
        version,
        fmt,
        collection_name,
        request.GET.get("view", None),
    )


def field(request, collection_name, key, field, fmt):
    field = urllib.parse.unquote_plus(field)
    if request.method == "GET":
        group = request.GET.get("group")
        admin = request.GET.get("admin")
        wiki = get_wiki_from_request(request, collection_name)
        document = get_document(
            group, admin, wiki, key, None, "dict", collection_name, None
        )

        value = document
        for level in field.split("||"):
            if isinstance(value, list):
                level = int(level)

            value = value[level]

        return JsonResponse(value, safe=False)
    elif request.method == "POST":
        post_fields = json.loads(request.body)
        group = post_fields["group"]
        wiki = get_wiki(post_fields, collection_name)
        new_value = post_fields["new_value"]
        edit_record(collection_name, key, group, wiki, field, new_value)
        return HttpResponse(201)


def get_attachments(request, collection_name, key, fmt):
    group = request.GET.get("group")
    admin = request.GET.get("admin")
    wiki = get_wiki_from_request(request, collection_name)

    attachments = []
    collection = models.Collection.objects.get(name=collection_name)
    document = collection.documents.get(key=key)

    if group:
        wiki_config = models.WikiConfig.objects.get(
            collection=collection,
            wiki=wiki,
            group=group,
        )
        attachments = []

        for potential_attachment in models.Attachment.objects.filter(document=document):
            if wiki_config.valid_fields.filter(
                id=potential_attachment.permissions_field.id
            ).exists():
                attachments.append(potential_attachment)
    elif admin:
        attachments = models.Attachment.objects.filter(document=document)

    if fmt == "json":
        return JsonResponse(
            [
                {
                    "name": a.name,
                    "size": a.file.size,
                }
                for a in attachments
            ],
            safe=False,
        )
    else:
        raise Exception(f"Invalid format {fmt}")


def get_attachment(request, collection_name, key, attachment):
    group = request.GET.get("group")
    admin = request.GET.get("admin")
    wiki = get_wiki_from_request(request, collection_name)
    attachment_name = secure_filename(urllib.parse.unquote_plus(attachment))

    collection = models.Collection.objects.get(name=collection_name)
    document = collection.documents.get(key=key)
    attachment = models.Attachment.objects.get(name=attachment_name, document=document)

    if group or not admin:
        wiki_config = models.WikiConfig.objects.get(
            collection=collection,
            wiki=wiki,
            group=group,
        )
        if not wiki_config.valid_fields.filter(
            id=attachment.permissions_field.id
        ).exists():
            raise Exception("Not permitted to see this attachment.")

    content_type = magic.from_buffer(attachment.file.open("rb").read(1024), mime=True)
    return FileResponse(
        attachment.file.open("rb"), filename=attachment_name, content_type=content_type
    )


def reset_config(request, collection_name, wiki_key):
    wiki = models.Wiki.objects.get_or_create(wiki_key=wiki_key)[0]
    wiki.username = None
    wiki.password = None
    wiki.script_path = None
    wiki.server = None
    wiki.linked_wiki_keys = list()
    wiki.save()

    models.WikiConfig.objects.filter(
        collection__name=collection_name, wiki=wiki
    ).update(in_config=False)

    models.Template.objects.filter(collection__name=collection_name, wiki=wiki).update(
        in_config=False
    )

    return HttpResponse(status=200)


@csrf_exempt
@require_http_methods(["POST"])
# Even though collection_name isn't user here, we add it so that the urls
# all nicely line up with the other config requests
def set_wiki_config(request, collection_name, wiki_key):
    wiki = models.Wiki.objects.get_or_create(wiki_key=wiki_key)[0]
    wiki_config = json.loads(request.body)
    wiki.username = wiki_config["username"]
    wiki.password = wiki_config["password"]
    wiki.script_path = wiki_config["script_path"]
    wiki.server = wiki_config["server"]
    wiki.linked_wiki_keys = wiki_config["linked_wiki_keys"]
    wiki.save()

    return HttpResponse(status=200)


@csrf_exempt
@require_http_methods(["POST"])
def set_group_config(request, collection_name, wiki_key):
    import hashlib

    new_config = json.loads(request.body)
    collection = models.Collection.objects.get(name=collection_name)
    wiki = models.Wiki.objects.get(wiki_key=wiki_key)

    try:
        config = models.WikiConfig.objects.get(
            collection=collection, wiki=wiki, group=new_config["group"]
        )
    except models.WikiConfig.DoesNotExist:
        config = None

    permissions_sha = hashlib.sha224(
        collection_name.encode("utf-8")
        + str(new_config.get("valid_ids")).encode("utf-8")
        + str(new_config.get("fields")).encode("utf-8")
    ).hexdigest()

    if config is None or permissions_sha != config.search_cache_sha:
        if config is not None:
            config.valid_ids.clear()
            config.valid_fields.clear()
        else:
            config = models.WikiConfig(
                collection=collection, wiki=wiki, group=new_config["group"]
            )
            config.save()

        for toc in collection.tables_of_contents.all():
            (cache, created) = models.TableOfContentsCache.objects.update_or_create(
                toc=toc, wiki_config=config
            )
            cache.dirty = True
            cache.save()

        config.search_cache_sha = permissions_sha

        valid_documents = models.Document.objects.filter(
            collection=collection, key__in=new_config.get("valid_ids")
        )
        valid_fields = models.Field.objects.filter(
            name__in=new_config.get("fields"), collection=collection
        )
        config.save()
        config.valid_ids.add(*valid_documents)
        config.valid_fields.add(*valid_fields)
        config.cache_dirty = True
        utils.dirty_documents(config.valid_ids.all(), config)

        for linked_wiki in models.Wiki.objects.filter(
            linked_wiki_keys__contains=[wiki_key]
        ):
            try:
                linked_wiki_config = models.WikiConfig.objects.get(
                    wiki=linked_wiki, group=config.group
                )
                models.TableOfContentsCache.objects.filter(
                    wiki_config=linked_wiki_config
                ).update(dirty=True)
            except models.WikiConfig.DoesNotExist:
                # If there's no proper config, do nothing
                pass

    config.in_config = True
    config.save()

    return HttpResponse(status=200)


def complete_config(request, collection_name, wiki_key):
    models.WikiConfig.objects.filter(
        collection__name=collection_name, wiki__wiki_key=wiki_key, in_config=False
    ).delete()
    models.Template.objects.filter(
        collection__name=collection_name, wiki__wiki_key=wiki_key, in_config=False
    ).delete()

    return HttpResponse(status=200)


@csrf_exempt
@require_http_methods(["POST"])
def set_template_config(request, collection_name, wiki_key):
    new_config = json.loads(request.body)

    conf_name = new_config["name"]
    conf_type = new_config["type"]
    default = new_config["default"]

    collection = models.Collection.objects.get(name=collection_name)
    wiki = models.Wiki.objects.get(wiki_key=wiki_key)
    template = models.Template.objects.get_or_create(
        collection=collection, wiki=wiki, type=conf_type, name=conf_name
    )[0]

    if template.get_file_contents() != new_config["template"]:
        template.template_file.save(
            f"{wiki_key}-{conf_name}", ContentFile(new_config["template"])
        )
        template.dirty = True

    template.in_config = True
    template.is_default = default
    template.save()

    return HttpResponse(status=200)


@csrf_exempt
@require_http_methods(["POST"])
def upload_collection(request):
    with request.FILES["data_file"].open(mode="rt") as f:
        collection, documents = models.Collection.from_json(
            name=request.POST["collection_name"],
            object_name=request.POST["object_name"],
            key_field=request.POST["key_field"],
            file=f,
        )
    collection.save()
    collection.templates.update(dirty=True)

    # Regenerate search caches in case data has changed.  We assume that the
    # cache is invalid, making uploading a collection be a very expensive operation,
    # but that's probably better than attempting to analyze cache invalidation
    # and failing.

    for config in models.WikiConfig.objects.filter(collection=collection):
        config.cache_dirty = True
        config.save()

    for wiki in models.Wiki.objects.filter(configs__collection=collection):
        wiki.invalidate_linked_wiki_toc_cache()

    return HttpResponse(status=200)


@csrf_exempt
@require_http_methods(["POST"])
def upload_toc(request):
    collection = models.Collection.objects.get(name=request.POST["collection_name"])
    (template, created) = models.Template.objects.update_or_create(
        collection=collection,
        type="uploaded_template",
        name=request.POST["toc_name"],
    )
    template.template_file = request.FILES["template"]
    template.save()
    json_file = request.FILES["json"].read().decode("utf-8")
    (toc, created) = models.TableOfContents.objects.update_or_create(
        collection=collection,
        name=request.POST["toc_name"],
        defaults={
            "json_file": json_file,
            "template": template,
        },
    )
    # Have to repeat this because we need to have it when we create, if
    # we do create (above), but we also need to set it in the case that
    # the TOC already exists in the database
    toc.json_file = json_file
    toc.template = template
    toc.raw = bool(request.POST["raw"])
    toc.save()

    for config in collection.configs.all():
        (cache, created) = models.TableOfContentsCache.objects.update_or_create(
            toc=toc,
            wiki_config=config,
        )
        cache.dirty = True
        cache.save()

    return HttpResponse(status=200)


@csrf_exempt
@require_http_methods(["POST"])
def upload_attachment(request):
    collection = models.Collection.objects.get(name=request.POST["collection_name"])
    permissions_field = models.Field.objects.get(
        collection=collection, name=request.POST["permissions_field"]
    )
    document = collection.documents.get(key=request.POST["object_id"])

    # Can't use update_or_create here because permissions field is not part
    # of the unique key (collection, name, document), but also not nullable,
    # so we have to manually do the update or create.
    try:
        attachment = models.Attachment.objects.get(
            collection=collection,
            name=secure_filename(request.POST["attachment_name"]),
            document=document,
        )
        attachment.permissions_field = permissions_field
    except models.Attachment.DoesNotExist:
        attachment = models.Attachment.objects.create(
            collection=collection,
            name=secure_filename(request.POST["attachment_name"]),
            document=document,
            permissions_field=permissions_field,
        )

    attachment.file = request.FILES["attachment"]
    attachment.save()

    return HttpResponse(status=200)


def user_by_username(request, username):
    # create user if doesn't exist
    try:
        user = models.User.objects.get(username=username)
    except models.User.DoesNotExist:
        user = models.User(username=username)
        user.save()

    return JsonResponse({"username": user.username, "id": user.pk})


@csrf_exempt
@require_http_methods(["POST"])
def add_csv(request):
    def determine_name():
        import string
        import random

        characters = string.ascii_lowercase + string.ascii_uppercase + string.digits
        possible_name = "".join([random.choice(characters) for i in range(6)])
        if models.CsvSpecification.objects.filter(name=possible_name).count() > 0:
            return determine_name()
        else:
            return possible_name

    name = determine_name()
    post_fields = json.loads(request.body)

    massive_or = Q()
    for post_doc in post_fields["documents"]:
        massive_or |= Q(collection__name=post_doc[0], key=post_doc[1])

    documents = models.Document.objects.filter(massive_or)

    csv_spec = models.CsvSpecification(
        name=name, filename=post_fields["filename"], fields=post_fields["fields"]
    )
    # Save first so the many to many below works correctly
    csv_spec.save()
    csv_spec.documents.set(documents)
    csv_spec.save()
    return JsonResponse(
        {
            "name": name,
        }
    )


def get_csv(request, name, fmt):
    csv_spec = models.CsvSpecification.objects.get(name=name)

    group = request.GET["group"]

    valid_documents = csv_spec.documents.filter(
        wiki_config__group=group
    ).prefetch_related("collection")

    if fmt == "json":
        document_information = {}
        for document in valid_documents:
            if document.collection.name not in document_information:
                document_information[document.collection.name] = []
            document_information[document.collection.name].append(document.key)
        return JsonResponse(
            {
                "name": name,
                "filename": csv_spec.filename,
                "fields": sorted(csv_spec.fields),
                "documents": document_information,
            }
        )
    elif fmt == "csv":
        csv_field_names = sorted(csv_spec.fields)

        wiki_configs_for_csv = models.WikiConfig.objects.filter(
            group=group, valid_ids__in=csv_spec.documents.all()
        ).distinct()

        valid_field_names = [
            field.name
            for field in models.Field.objects.filter(
                wiki_config__in=wiki_configs_for_csv
            ).distinct()
        ]

        field_names = [fn for fn in csv_field_names if fn in valid_field_names]

        response = HttpResponse(
            content_type="text/csv",
            headers={
                "Content-Disposition": 'attachment; filename="%s.csv"'
                % csv_spec.filename
            },
        )
        writer = csv.writer(response)

        columns = []
        for field_name in field_names:
            if field_name in getattr(settings, "TORQUE_CSV_PROCESSORS", {}):
                columns.extend(
                    settings.TORQUE_CSV_PROCESSORS[field_name].field_names(field_name)
                )
            else:
                columns.append(field_name)
        writer.writerow(columns)

        all_pertinent_values = (
            models.Value.objects.filter(
                field__name__in=field_names, document__in=valid_documents
            )
            .prefetch_related("field")
            .prefetch_related("document")
        )

        values_by_documents_and_fields = {}

        for value in all_pertinent_values:
            if value.document not in values_by_documents_and_fields:
                values_by_documents_and_fields[value.document] = {}
            values_by_documents_and_fields[value.document][value.field.name] = value

        for document in valid_documents:
            row = []
            values_by_field = values_by_documents_and_fields[document]
            for field_name in field_names:
                python_value = None
                if field_name in values_by_field:
                    python_value = values_by_field[field_name].to_python()
                if python_value and field_name in getattr(
                    settings, "TORQUE_CSV_PROCESSORS", {}
                ):
                    row.extend(
                        settings.TORQUE_CSV_PROCESSORS[field_name].process_value(
                            python_value
                        )
                    )
                elif field_name in getattr(settings, "TORQUE_CSV_PROCESSORS", {}):
                    row.extend(
                        settings.TORQUE_CSV_PROCESSORS[field_name].default_value(
                            field_name
                        )
                    )
                elif python_value:
                    row.append(python_value)
                else:
                    row.append("")
            writer.writerow(row)

        return response
    else:
        raise Exception(f"Invalid format {fmt}")
