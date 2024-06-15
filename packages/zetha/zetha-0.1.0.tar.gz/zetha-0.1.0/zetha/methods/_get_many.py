# -*- coding: utf-8 -*-
# pylint: disable=missing-module-docstring
from typing import Any, Iterable
from requests import get # type: ignore

def get_many(url: str, headers: dict[str, str], ids: Iterable[Any]) -> list[dict[str, Any]]:
    if '{id}' not in url:
        raise ValueError("Url informada deve conter o placeholder '{id}'")

    response: list[dict[str, Any]] = []
    for identifier in ids:
        request = get(url.format(id=identifier), headers=headers) # pylint: disable=missing-timeout
        response.append(request.json())
    return response
