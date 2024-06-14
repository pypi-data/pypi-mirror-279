from typing import Dict, List, Union, Optional

from dooray_api_wrapper.common import dooray_request
from dooray_api_wrapper.structure import response_result, response_header


def get_wiki_list() -> Optional[response_result.WikiResult]:
    """접근 가능한 위키 목록을 조회합니다."""
    end_point = f"/wiki/v1/wikis"
    params = {
        "page": 0,
        "size": 100,
    }

    data = dooray_request.dooray_get(end_point, params)
    if data is None:
        return None

    def response(
        data: Dict,
    ) -> Optional[
        List[Union[response_header.ResponseHeader, response_result.WikiResult]]
    ]:
        if "header" not in data or "result" not in data:
            return None

        header = response_header.ResponseHeader(**data["header"])
        result = {"result": data["result"]}
        return [header, response_result.WikiResult(**result)]

    [header, wiki_list] = response(data)
    cnt = len(wiki_list.result)
    if "totalCount" not in data:
        return wiki_list

    total_count = data["totalCount"]

    while cnt < total_count:
        params["page"] += 1
        data = dooray_request.dooray_get(end_point, params)
        if data is None:
            return wiki_list

        [header, result] = response(data)
        wiki_list.result.extend(result.result)
        cnt = len(wiki_list.result)

    return wiki_list


def get_wiki_sub_pages(
    wiki_id: str, parentPageId: Optional[str] = None
) -> Optional[response_result.WikiPageResult]:
    """특정 위키 페이지의 하위 페이지들을 조회합니다."""
    end_point = f"/wiki/v1/wikis/{wiki_id}/pages"
    params = {
        "parentPageId": parentPageId,
    }
    data = dooray_request.dooray_get(end_point, params)
    if data is None:
        return None

    header = data["header"]
    result = {"result": data["result"]}
    return response_result.WikiPageResult(**result)


def get_wiki_page(
    wiki_id: str, pageId: str
) -> Optional[response_result.WikiPageResultItem]:
    """특정 위키 페이지를 조회합니다."""
    end_point = f"/wiki/v1/wikis/{wiki_id}/pages/{pageId}"
    response = dooray_request.dooray_get(end_point)
    if response is None:
        return None

    header = response["header"]
    result = response["result"]
    return response_result.WikiPageResultItem(**result)
