from rest_framework.response import Response
from rest_framework import status


def create_200_response(message, data=None):

    return Response(
        {
            'status': True,
            'status_code': status.HTTP_200_OK,
            'message': message,
            'data': data or {}
        },
        status=status.HTTP_200_OK
    )

def create_201_response(message, data=None):

    return Response(
        {
            'status': True,
            'status_code': status.HTTP_201_CREATED,
            'message': message,
            'data': data or {}
        },
        status=status.HTTP_201_CREATED
    )

def create_204_response(message, data=None):

    return Response(
        {
            'status': True,
            'status_code': status.HTTP_204_NO_CONTENT,
            'message': message,
            'data': data or {}
        },
        status=status.HTTP_204_NO_CONTENT
    )

def create_205_response(message, data=None):

    return Response(
        {
            'status': True,
            'status_code': status.HTTP_205_RESET_CONTENT,
            'message': message,
            'data': data or {}
        },
        status=status.HTTP_205_RESET_CONTENT
    )

def create_400_response(message, data=None):

    return Response(
        {
            'status': False,
            'status_code': status.HTTP_400_BAD_REQUEST,
            'message': message,
            'data': data or {}
        },
        status=status.HTTP_400_BAD_REQUEST
    )

def create_401_response(message, data=None):

    return Response(
        {
            'status': True,
            'status_code': status.HTTP_401_UNAUTHORIZED,
            'message': message,
            'data': data or {}
        },
        status=status.HTTP_401_UNAUTHORIZED
    )

def create_403_response(message, data=None):

    return Response(
        {
            'status': True,
            'status_code': status.HTTP_403_FORBIDDEN,
            'message': message,
            'data': data or {}
        },
        status=status.HTTP_403_FORBIDDEN
    )

def create_404_response(message, data=None):

    return Response(
        {
            'status': True,
            'status_code': status.HTTP_404_NOT_FOUND,
            'message': message,
            'data': data or {}
        },
        status=status.HTTP_404_NOT_FOUND
    )

def create_405_response(message, data=None):

    return Response(
        {
            'status': True,
            'status_code': status.HTTP_405_METHOD_NOT_ALLOWED,
            'message': message,
            'data': data or {}
        },
        status=status.HTTP_405_METHOD_NOT_ALLOWED
    )