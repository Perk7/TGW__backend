import datetime
import random
from typing import Literal

from django.core.mail import send_mail

from django.db.utils import OperationalError
from django.conf import settings

from .models_auth import CustomAuth
from django.shortcuts import get_object_or_404

from django.contrib.auth.hashers import check_password

mail_types = Literal['Password Recovery', 'Verification Code']
def send_mail_with_code(mail: str, type: mail_types) -> int:
    """
    Sending mail to user with verification code
    """
    code = str(random.randint(1000,9999))

    hash_msg = {
        'Password Recovery': f'\nВаш код для восстановления пароля: {code}\nПочта: {mail}',
        'Verification Code': f'\nПочта: {mail}\nВаш код подтверждения электронной почты: {code}\n.'
    }

    send_mail(type, str(datetime.datetime.now()) + hash_msg[type], settings.EMAIL_HOST_USER,
              [mail], fail_silently=False)

    return code

def check_email_for_uniq(mail: str) -> str:
    """
    Check uniqness of email in db, and sending message for confirm. Return code for confirm.
    """
    try:
        users = CustomAuth.objects.all()
    except OperationalError:
        return ''

    emails = [i.email for i in users]
    
    if mail not in emails:
        code = send_mail_with_code(mail, 'Verification Code')
        return code
    else:
        return ''

def registrate_with_values(data: dict) -> dict:
    """
    Try to registrate user with credentials and return logs of it
    """
    logs = {
        'login': False,
        'email': False,
        'success': False
    }

    try:
        users = CustomAuth.objects.all()
        usernames = [i.username for i in users]
        emails = [i.email for i in users]
        if data and data['login'] not in usernames and data['email'] not in emails:
            user = CustomAuth.objects.create_user(data['login'], data['email'], data['password'])
            user.save()
            logs['success'] = True
        logs['login'] = data['login'] not in usernames
        logs['email'] = data['email'] not in emails

    except OperationalError:
        pass

    return logs

def change_password_after_confirm_mail(data: dict) -> bool:
    '''
    Changing password to new, after confirming email
    '''
    status = False

    mail = data['mail']
    try:
        user = get_object_or_404(CustomAuth, email=mail)
        user.set_password(data['password'])
        user.save()
        status = True
    except OperationalError:
        return status
    
    return status

def try_send_confirm_email_code(mail: str) -> str:
    """
    Sending mail with verification code to confirm email for changing password
    """
    code = ''
    try:
        users = CustomAuth.objects.all()
    except OperationalError:
        return code

    emails = [i.email for i in users]
    if mail in emails:
        code = send_mail_with_code(mail, 'Password Recovery')
    return code

def check_condition_for_login(authorizied: bool, data: dict) -> dict:
    '''
    Check conditions for login user and return status with user Object or Fasle
    '''
    status = 'already' if authorizied else 'wrong'
    user = False
    if not authorizied:
        try:
            if data['login'] in [i.username for i in CustomAuth.objects.all()]:
                user = get_object_or_404(CustomAuth, username=data['login'])
                checking = check_password(data['password'], user.password)
                status = 'success' if checking else 'wrong'

        except OperationalError:
            status = 'wrong'

    return {
        'status': status,
        'user': user
    }