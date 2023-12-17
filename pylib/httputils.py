class RestApiResponse:
    def __init__(self, content, status_code):
        self.content = content
        self.status_code = status_code