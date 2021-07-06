from django.conf import settings
from django.core.mail import send_mail
import random
from django.contrib.auth import login, logout
from rest_framework.decorators import api_view
import json
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
from django.contrib.auth.hashers import check_password
from .models_auth import CustomAuth
import datetime

from django.db.utils import OperationalError

@api_view(['POST'])
def check_email(request):
    try:
        users = CustomAuth.objects.all()
    except OperationalError:
        pass
    emails = [i.email for i in users]

    mail = request.data['mail']
    if mail not in emails:
        code = str(random.randint(1000,9999))
        send_mail('Verification Code', f'{datetime.datetime.now()}\nПочта: {mail}\nВаш код подтверждения электронной почты: {code}\n.', settings.EMAIL_HOST_USER,
                  [mail], fail_silently=False)
        return Response(json.dumps({
            'status': True,
            'code': code
        }), status=status.HTTP_201_CREATED)
    else:
        return Response(json.dumps({
            'status': False
        }), status=status.HTTP_201_CREATED)


@api_view(['POST'])
def registration(request):
    post = request.data
    try:
        users = CustomAuth.objects.all()
        usernames = [i.username for i in users]
        emails = [i.email for i in users]
        if post and post['login'] not in usernames and post['email'] not in emails:
            user = CustomAuth.objects.create_user(post['login'], post['email'], post['password'])
            user.save()
            return Response(json.dumps({
                'status' : True,
                'login' : post['login'] not in usernames,
                'email' : post['email'] not in emails,
            }), status=status.HTTP_201_CREATED)
        else:
            return Response(json.dumps({
                'status' : False,
                'login': post['login'] not in usernames,
                'email': post['email'] not in emails,
            }), status=status.HTTP_201_CREATED)
    except OperationalError:
            pass

@api_view(['POST'])
def try_login(request):
    if not request.user.is_authenticated:
        post = request.data
        try:
            if CustomAuth.objects.filter(username=post['login']):
                user = get_object_or_404(CustomAuth, username=post['login'])
                checking = check_password(post['password'], user.password)
                if checking:
                    login(request, user)
                    return Response(json.dumps({
                        'status': 'success',
                        'log': request.user.isauthenticated
                    }), status=status.HTTP_201_CREATED)
                else:
                    return Response(json.dumps({
                        'status': 'wrong',
                    }), status=status.HTTP_201_CREATED)
        except OperationalError:
            pass
        else:
            return Response(json.dumps({
                'status': 'wrong',
                'log': request.user.is_authenticated
            }), status=status.HTTP_201_CREATED)
    else:
        return Response(json.dumps({
            'status': 'already',
        }), status=status.HTTP_201_CREATED)

@api_view(['GET'])
def try_logout(request):
    """
 	Return all Countries
 	"""
    if request.method == 'GET':
        logout(request)
        return Response(status=status.HTTP_201_CREATED)

@api_view(['POST'])
def recovery_password(request):
    mail = request.data['mail']
    try:
        user = get_object_or_404(CustomAuth, email=mail)
    except OperationalError:
        pass
    user.set_password(request.data['password'])
    user.save()
    return Response(json.dumps({
            'status': 'success'
        }), status=status.HTTP_201_CREATED)

@api_view(['POST'])
def recovery_password_code(request):
    try:
        users = CustomAuth.objects.all()
    except OperationalError:
        pass
    emails = [i.email for i in users]
    mail = request.data['mail']
    if mail in emails:
        code = str(random.randint(1000,9999))
        print(mail)
        send_mail('Password Recovery', f'Ваш код для восстановления пароля: {code}\nПочта: {mail}', settings.EMAIL_HOST_USER,
                  [mail], fail_silently=False)
        return Response(json.dumps({
            'status': 'success',
            'code': code
        }), status=status.HTTP_201_CREATED)
    else:
        return Response(json.dumps({
            'status': 'wrong'
        }), status=status.HTTP_201_CREATED)