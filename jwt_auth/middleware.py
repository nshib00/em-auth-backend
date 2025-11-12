from django.http import JsonResponse

class AuthFailedHandlingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if response.status_code == 403:
            user = getattr(request, 'user', None)
            if not user or not getattr(user, 'is_authenticated', False):
                return JsonResponse(
                    {'detail': 'Token not provided.'},
                    status=401
                )
        return response
