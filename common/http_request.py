import json

from httper.common.inet.layers.l7 import HTTP


class Request:
    def __init__(self, http_raw: HTTP):
        self.method = http_raw.method
        self.url = http_raw.path
        if '?' in http_raw.path:
            path, query_params = http_raw.path.split('?')
            self.query = {query_param[0: query_param.find('=')]: query_param[query_param.find('=') + 1:] for query_param
                          in query_params.split('&')}
        else:
            path = http_raw.path
            self.query = {}
        self.path = path
        self.protocol = http_raw.protocol
        self.params = {}
        self.body = http_raw.body

    def __str__(self):
        return json.dumps({'path': self.path, 'query': self.query, 'params': self.params, 'body': self.body})