"""Main module."""
from typing import List

from .path import OpenApiPath
from .utils import get_openapi_schema, get_openapi_type


class OpenApi():

    version = '3.0.2'
    title = None
    paths = None

    def __init__(self,
                 title: str,
                 paths: List[OpenApiPath]):
        self.title = title
        self.paths = paths

    def asdict(self):
        openapi_dict = {
            'openapi': self.version,
            'info': {
                'title': self.title,
                'version': self.version
            },
            'paths': {
            },
            'components': {
                'schemas': {}
            }
        }
        for openapi_path in self.paths:
            if openapi_dict['paths'].get(openapi_path.path) is None:
                openapi_dict['paths'][openapi_path.path] = {}
            openapi_dict['paths'][openapi_path.path].update(
                openapi_path.asdict()[openapi_path.path])

            for param in openapi_path.params:
                if get_openapi_type(param.data_type) == 'object':
                    openapi_dict['components']['schemas'] = get_openapi_schema(
                        param.data_type)

            for resp in openapi_path.responses:
                if get_openapi_type(resp.data_type) == 'object':
                    openapi_dict['components']['schemas'] = get_openapi_schema(
                        resp.data_type)

        return openapi_dict
