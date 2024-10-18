from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
# from oauthlib.oauth2.rfc6749.errors import InsecureTransportError
from rest_framework.exceptions import (AuthenticationFailed, MethodNotAllowed,
                                       NotAuthenticated, NotFound,
                                       PermissionDenied, Throttled,
                                       ValidationError)
from rest_framework.response import Response
from rest_framework.views import exception_handler

from wallet.custom_exception import CustomValidationException


def custom_exception_handler(exc, context):
    """
    Custom exception handler for handling various exceptions and returning appropriate responses.

    Args:
        exc (Exception): The raised exception.
        context (dict): Context information about the exception.

    Returns:
        Response: The response object containing the error message and status code.

    Raises:
        None
    """
    from rest_framework import status
    if isinstance(exc, AuthenticationFailed):
        return Response({'status': False, 'msg': 'Kindly logout and login again'}, status=status.HTTP_401_UNAUTHORIZED)

    if isinstance(exc, ObjectDoesNotExist):
        return Response({'status': False, 'msg': 'This resource doesn\'t exist'}, status=status.HTTP_404_NOT_FOUND)
    # if isinstance(exc, TypeError):
    #     # print(exc)
    #     return Response({'status': False, 'msg': 'Data could not be parsed'}, status=status.HTTP_400_BAD_REQUEST)

    # if isinstance(exc, InsecureTransportError):
    #     if 'OAuth 2 MUST utilize' in str(exc):
    #         return Response({'status': False, 'msg': 'Refer to the system administrator about using a valid SSL for this request.', }, status=status.HTTP_400_BAD_REQUEST)

    if isinstance(exc, IntegrityError):
        if 'Duplicate entry' in str(exc):
            return Response({'status': False, 'msg': 'Duplicate entry in the data supplied', }, status=status.HTTP_400_BAD_REQUEST)

    if isinstance(exc, Throttled):
        return Response({'status': False, 'msg': 'Too many requests from your account. Kindly wait a while.'}, status=exc.status_code)

    if isinstance(exc, CustomValidationException):
        status = False
        if exc.status_code < 400:
            status = True
        return Response({'status': status, 'msg': exc.detail}, status=exc.status_code)

    if isinstance(exc, TypeError):
        if "required positional argument: 'pk'" in str(exc):
            return Response({'status': False, 'msg': 'Invalid data - Make sure to read the documentation before using this endpoint.'}, status=status.HTTP_406_NOT_ACCEPTABLE)
    if isinstance(exc, PermissionDenied):
        if 'You do not have permission to perform this action' in str(exc):
            return Response({'status': False, 'msg': 'You do not have sufficient access'}, status=status.HTTP_403_FORBIDDEN)

    if isinstance(exc, (AuthenticationFailed, NotAuthenticated)):
        if 'invalid_token' in str(exc) or 'Token is invalid or expired' in str(exc):
            return Response({'status': False, 'msg': 'Your session must have either expired or been invalidated. Please log out and login again.'}, status=status.HTTP_401_UNAUTHORIZED)
        elif 'missing_token' in str(exc) or 'Authentication credentials were not provided' in str(exc):
            return Response({'status': False, 'msg': 'Access to this page is restricted.'}, status=status.HTTP_401_UNAUTHORIZED)
        elif 'active account found with the given credentials' in str(exc):
            return Response({'status': False, 'msg': 'Invalid parameters'}, status=status.HTTP_401_UNAUTHORIZED)

        elif 'Given token not valid for any token type' in str(exc):
            messages = exc.detail.get('messages', None)
            if messages:
                message = messages[0]['message']
                return Response({'status': False, 'msg': message}, status=status.HTTP_401_UNAUTHORIZED)
    if isinstance(exc, ValidationError):
        if 'field is required' in str(exc):
            return Response({'status': False, 'msg': 'Please fill all required fields', 'fields': exc.detail}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'status': False, 'msg': 'Invalid data sent', 'fields': exc.detail}, status=status.HTTP_400_BAD_REQUEST)

    if isinstance(exc, NotFound):
        return Response({'status': False, 'msg': 'The resource you are looking for has been removed, had its name changed, or is temporarily unavailable.', }, status=status.HTTP_404_NOT_FOUND)

    if isinstance(exc, MethodNotAllowed):
        return Response({'status': False, 'msg': 'Page not found.'}, status=status.HTTP_404_NOT_FOUND)

    return exception_handler(exc, context)
