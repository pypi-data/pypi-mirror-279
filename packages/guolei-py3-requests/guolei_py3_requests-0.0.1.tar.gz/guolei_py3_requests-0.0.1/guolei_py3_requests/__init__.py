#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
=================================================
requests Class Library
-------------------------------------------------
作者：[郭磊]
手机：[15210720528]
Email：[174000902@qq.com]
Github：https://github.com/guolei19850528/guolei_py3_requests
=================================================
"""
import typing
from inspect import isfunction
from typing import Union, Iterable, Callable
import requests
from addict import Dict
from requests import Response, Session


def requests_request(
        requests_response_callable: Callable[[Response], typing.Any] = None,
        requests_request_args: Union[Iterable] = (),
        requests_request_kwargs: Union[dict, Dict] = Dict({})
):
    """
    call requests.request
    :param requests_response_callable: if isfunction(requests_response_callable) return requests_response_callable(session,response) else return response
    :param requests_request_args: requests.request(*requests_request_args,**requests_request_kwargs)
    :param requests_request_kwargs: requests.request(*requests_request_args,**requests_request_kwargs)
    :return: if isfunction(requests_response_callable) return requests_response_callable(session,response) else return response
    """
    requests_request_kwargs = Dict(requests_request_kwargs)
    response = requests.request(*requests_request_args, **requests_request_kwargs.to_dict())
    if not isinstance(requests_response_callable, Callable):
        return response
    else:
        return requests_response_callable(response=response)


def request_session_request(
        session: Session = None,
        requests_response_callable: Callable[[Session, Response], typing.Any] = None,
        requests_request_args: Union[Iterable] = (),
        requests_request_kwargs: Union[dict, Dict] = Dict({})
):
    """
    call requests.Session.request
    :param session: requests.Session
    :param requests_response_callable: if isfunction(requests_response_callable) return requests_response_callable(session,response) else return response
    :param requests_request_args: requests.request(*requests_request_args,**requests_request_kwargs)
    :param requests_request_kwargs: requests.request(*requests_request_args,**requests_request_kwargs)
    :return: if isfunction(requests_response_callable) return requests_response_callable(session,response) else return response
    """
    requests_request_kwargs = Dict(requests_request_kwargs)
    response = session.request(*requests_request_args, **requests_request_kwargs.to_dict())
    if not isfunction(requests_response_callable):
        return session, response
    else:
        return requests_response_callable(session, response)
