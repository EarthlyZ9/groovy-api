from django.http import JsonResponse


class Response(JsonResponse):
    def __init__(self, status=2001, data=None, error=None, http_status=200):
        super().__init__(data=dict(status=status, data=data, error=error), safe=False, status=http_status)
