# -*- coding: utf-8 -*-
# pylint: disable=missing-module-docstring
from typing import Any, Iterable
from asyncio import create_task, gather, run
from aiohttp import ClientSession

async def _async_get_one(session: ClientSession, url: str, headers: dict[str, str], identifier: Any) -> dict[str, Any]:
    async with session.get(url.format(id=identifier), headers=headers) as response:
        return await response.json()

async def _async_get_many(url: str, headers: dict[str, str], ids: Iterable[Any]) -> list[dict[str, Any]]:
    async with ClientSession() as session:
        requests: list[Any] = []
        for identifier in ids:
            request = create_task(_async_get_one(session, url, headers, identifier))
            requests.append(request)
        responses: list[dict[str, Any]] = await gather(*requests)
        return responses

def async_get(url: str, headers: dict[str, str], ids: Iterable[Any]) -> list[dict[str, Any]]:
    """Obtém dados de várias URLs assíncronas usando uma lista de identificadores, de forma síncrona.

    ### Args:
        url (str): URL com um placeholder para os identificadores.
        headers (dict[str, str]): Cabeçalhos HTTP a serem enviados na requisição.
        ids (Iterable[Any]): lista de identificadores a serem formatados na URL.

    ### Returns:
        list[dict[str, Any]]: lista de respostas JSON das requisições.

    ### Raises:
        ValueError: Se a URL não contiver o placeholder '{id}'.

    ### Examples:
        ```python
        url: str = 'http://example.com/resource/{id}'
        headers: dict[str, str] = {'Authorization': 'Bearer token'}
        ids: list[int] = [123, 456, 789]
        
        # Reliza get requests de forma assincrona buscando pelos ids [123, 456, 789]
        data: list[dict[str, Any]] = async_get(url, headers, ids)
        ```
    """
    if '{id}' not in url:
        raise ValueError("Url informada deve conter o placeholder '{id}'")
    return run(_async_get_many(url, headers, ids))
