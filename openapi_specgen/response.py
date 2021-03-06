from .utils import get_openapi_type


class OpenApiResponse():

    def __init__(self,
                 descr: str,
                 status_code: str = '200',
                 data_type: type = None,
                 http_content_type: str = 'application/json'):
        self.descr = descr
        self.data_type = data_type
        self.status_code = status_code
        self.http_content_type = http_content_type

    def asdict(self):
        openapi_dict = {
            self.status_code: {
                'description': self.descr
            }
        }

        if self.data_type is None:
            return openapi_dict

        openapi_type = get_openapi_type(self.data_type)

        if openapi_type == 'object':
            openapi_dict[self.status_code]['content'] = {
                self.http_content_type: {
                    'schema': {
                        '$ref': f'#/components/schemas/{self.data_type.__name__}'
                    }
                }
            }
        else:
            openapi_dict[self.status_code]['content'] = {
                self.http_content_type: {
                    'schema': {'type': openapi_type}
                }
            }
        return openapi_dict
