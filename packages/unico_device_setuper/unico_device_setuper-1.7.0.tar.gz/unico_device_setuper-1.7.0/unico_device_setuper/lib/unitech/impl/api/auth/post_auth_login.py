from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.login_choose_response import LoginChooseResponse
from ...models.login_payload import LoginPayload
from ...models.login_token_response import LoginTokenResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    
    body: LoginPayload,
    authorization: Union[None, Unset, str] = UNSET,
) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}
    if not isinstance(authorization, Unset):
        headers["authorization"] = authorization

    _kwargs: Dict[str, Any] = {
        "method": "post",
        "url": "/auth/login",
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
     client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Union["LoginChooseResponse", "LoginTokenResponse"], str]]:
    if response.status_code == HTTPStatus.OK:

        def _parse_response_200(data: object) -> Union["LoginChooseResponse", "LoginTokenResponse"]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                response_200_type_0 = LoginTokenResponse.from_dict(data)

                return response_200_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            response_200_type_1 = LoginChooseResponse.from_dict(data)

            return response_200_type_1

        response_200 = _parse_response_200(response.json())

        return response_200
    if response.status_code == HTTPStatus.UNAUTHORIZED:
        response_401 = cast(str, response.json())
        return response_401
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
     client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Union["LoginChooseResponse", "LoginTokenResponse"], str]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    
    client: Union[AuthenticatedClient, Client],
    body: LoginPayload,
    authorization: Union[None, Unset, str] = UNSET,
) -> Response[Union[Union["LoginChooseResponse", "LoginTokenResponse"], str]]:
    """
    Args:
        authorization (Union[None, Unset, str]):
        body (LoginPayload):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Union['LoginChooseResponse', 'LoginTokenResponse'], str]]
    """

    kwargs = _get_kwargs(
        body=body,
        authorization=authorization,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    
    client: Union[AuthenticatedClient, Client],
    body: LoginPayload,
    authorization: Union[None, Unset, str] = UNSET,
) -> Optional[Union[Union["LoginChooseResponse", "LoginTokenResponse"], str]]:
    """
    Args:
        authorization (Union[None, Unset, str]):
        body (LoginPayload):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Union['LoginChooseResponse', 'LoginTokenResponse'], str]
    """

    return sync_detailed(
        client=client,
        body=body,
        authorization=authorization,
    ).parsed


async def detailed_request(
    
    client: Union[AuthenticatedClient, Client],
    body: LoginPayload,
    authorization: Union[None, Unset, str] = UNSET,
) -> Response[Union[Union["LoginChooseResponse", "LoginTokenResponse"], str]]:
    """
    Args:
        authorization (Union[None, Unset, str]):
        body (LoginPayload):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Union['LoginChooseResponse', 'LoginTokenResponse'], str]]
    """

    kwargs = _get_kwargs(
        body=body,
        authorization=authorization,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def request(
    
    client: Union[AuthenticatedClient, Client],
    body: LoginPayload,
    authorization: Union[None, Unset, str] = UNSET,
) -> Optional[Union[Union["LoginChooseResponse", "LoginTokenResponse"], str]]:
    """
    Args:
        authorization (Union[None, Unset, str]):
        body (LoginPayload):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Union['LoginChooseResponse', 'LoginTokenResponse'], str]
    """

    return (
        await detailed_request(
            client=client,
            body=body,
            authorization=authorization,
        )
    ).parsed
