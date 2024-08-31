from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.audio_metadata import AudioMetadata
from ...models.http_validation_error import HTTPValidationError
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    file_url: str,
    max_duration: Union[Unset, float] = 90.0,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}

    params["file_url"] = file_url

    params["max_duration"] = max_duration

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": "/analyze",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[AudioMetadata, HTTPValidationError]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = AudioMetadata.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[AudioMetadata, HTTPValidationError]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    file_url: str,
    max_duration: Union[Unset, float] = 90.0,
) -> Response[Union[AudioMetadata, HTTPValidationError]]:
    """Audio

    Args:
        file_url (str):
        max_duration (Union[Unset, float]):  Default: 90.0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[AudioMetadata, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        file_url=file_url,
        max_duration=max_duration,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    file_url: str,
    max_duration: Union[Unset, float] = 90.0,
) -> Optional[Union[AudioMetadata, HTTPValidationError]]:
    """Audio

    Args:
        file_url (str):
        max_duration (Union[Unset, float]):  Default: 90.0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[AudioMetadata, HTTPValidationError]
    """

    return sync_detailed(
        client=client,
        file_url=file_url,
        max_duration=max_duration,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    file_url: str,
    max_duration: Union[Unset, float] = 90.0,
) -> Response[Union[AudioMetadata, HTTPValidationError]]:
    """Audio

    Args:
        file_url (str):
        max_duration (Union[Unset, float]):  Default: 90.0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[AudioMetadata, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        file_url=file_url,
        max_duration=max_duration,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    file_url: str,
    max_duration: Union[Unset, float] = 90.0,
) -> Optional[Union[AudioMetadata, HTTPValidationError]]:
    """Audio

    Args:
        file_url (str):
        max_duration (Union[Unset, float]):  Default: 90.0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[AudioMetadata, HTTPValidationError]
    """

    return (
        await asyncio_detailed(
            client=client,
            file_url=file_url,
            max_duration=max_duration,
        )
    ).parsed
