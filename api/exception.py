from rest_framework import status
from rest_framework.views import exception_handler as drf_exception_handler
from rest_framework.views import Response


def exception_handler(exc, context):
    response = drf_exception_handler(exc, context)
    print("%s - %s - %s" % (context['view'], context['request'].method, exc))
    error = "%s - %s - %s" % (context['view'], context['request'].method, exc)
    if response is None:
        return Response({
            "error": "程序错误"
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR, exception=None)
    return response
