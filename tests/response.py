class MyResponse:
    def __init__(self, response):
        self.response = response
        self.response_json = response.json()

    def validate(self, schema):
        if isinstance(self.response_json, list):
            for item in self.response_json:
                schema(**item)
        else:
            schema(**self.response_json)
        return self

    def assert_json(self, expected_obj):
        assert self.response_json == expected_obj, self
        return self

    def assert_len(self, length):
        assert len(self.response_json) == length, self
        return self

    def assert_status_code(self, status):
        if isinstance(status, list):
            assert self.response.status_code in status, self
        else:
            assert self.response.status_code == status, self
        return self

    def __str__(self):
        return f"""
        status_code={self.response.status_code}
        json={self.response_json}
        request={self.response.request}
"""
