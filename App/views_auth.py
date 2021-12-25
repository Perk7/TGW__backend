import json

from django.contrib.auth import login, logout

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .services_auth import *
from .decorators_views import check_api_key

@api_view(['POST'])
def check_email(request):
    """
    Check having email in db
    """
    mail = request.data['mail']
    code = check_email_for_uniq(mail)
    
    return Response(json.dumps({
            'status': bool(code),
            'code': code
        }), status=status.HTTP_201_CREATED if code else status.HTTP_208_ALREADY_REPORTED)
        
@api_view(['POST'])
def registration_in_system(request):
    """
    Registration in system with login, email and password
    """
    post = request.data
    auth_status = registrate_with_values(post)

    return Response(json.dumps({
                'status' : auth_status['success'],
                'login' : auth_status['login'],
                'email' : auth_status['email'],
            }), status=status.HTTP_201_CREATED if auth_status['success'] else status.HTTP_200_OK)

@api_view(['POST'])
def try_login(request):
    """
    Check conditions for login and do it, if check are success
    """
    result = check_condition_for_login(request.user.is_authenticated, request.data)

    if result['status'] == 'success':
        login(request, result['user'])

    return Response(json.dumps({
        'status': result['status'],
        'log': request.user.isauthenticated
    }), status=status.HTTP_201_CREATED if result['status'] == 'success' else status.HTTP_200_OK)

@api_view(['GET'])
@check_api_key
def try_logout(request):
    """
 	Logout user from system
 	"""
    logout(request)

    return Response(status=status.HTTP_200_OK)

@api_view(['POST'])
def recovery_password(request):
    """
    Change password of user
    """
    success = change_password_after_confirm_mail(request.data)

    return Response(json.dumps({
            'status': 'success' if success else 'fail'
        }), status=status.HTTP_201_CREATED if success else status.HTTP_200_OK)

@api_view(['POST'])
def recovery_password_code(request):
    """
    Sending email to confirm the email
    """
    code = try_send_confirm_email_code(request.data['mail'])

    return Response(json.dumps({
        'status': 'success' if code else 'wrong',
        'code': code
    }), status=status.HTTP_201_CREATED if code else status.HTTP_200_OK)