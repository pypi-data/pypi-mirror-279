from typing import Dict, List, Union, Optional

from dooray_api_wrapper.common import dooray_request
from dooray_api_wrapper.const.const import Scope, Type, State
from dooray_api_wrapper.structure import response_result, response_header


def get_project_list(
    scope: Scope = Scope.PUBLIC,
    type: Type = Type.PUBLIC,
    state: State = State.ACTIVE,
) -> Optional[response_result.ProjectResult]:
    """접근 가능한 프로젝트 목록을 조회합니다."""
    end_point = f"/project/v1/projects"
    params = {
        "page": 0,
        "size": 20,
        "scope": scope.value,
        "type": type.value,
        "state": state.value,
    }

    data = dooray_request.dooray_get(end_point, params)
    if data is None:
        return None

    [header, project_list] = response(data)
    cnt = len(project_list.result)
    if "totalCount" not in data:
        return project_list

    total_count = data["totalCount"]

    while cnt < total_count:
        params["page"] += 1
        data = dooray_request.dooray_get(end_point, params)
        if data is None:
            return project_list

        [header, result] = response(data)
        project_list.result.extend(result.result)
        cnt = len(project_list.result)

    return project_list


def get_project(project_id: str) -> Optional[response_result.ProjectResult]:
    end_point = f"/project/v1/projects/{project_id}"
    data = dooray_request.dooray_get(end_point)
    if data is None:
        return None
    [header, project] = response(data)
    return project


def response(
    data: Dict,
) -> Optional[
    List[Union[response_header.ResponseHeader, response_result.ProjectResult]]
]:
    if "header" not in data or "result" not in data:
        return None

    header = data["header"]
    result = {"result": data["result"]}
    return [
        response_header.ResponseHeader(**header),
        response_result.ProjectResult(**result),
    ]
