import re
import json
import jwt

from django.http import JsonResponse

from user.models import User
from my_settings import SECRET_KEY, ALGORITHM

def authorize_decorator(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            token=request.headers.get("Authorization")
            payload=jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
            request.user=payload['user_id']
        except jwt.exceptions.DecodeError:
            return JsonResponse({'message': 'INVALID TOKEN'}, status=400)

        return func(self, request, *args, **kwargs)
    return wrapper

def signup_validator(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            data             = json.loads(request.body)
            email            = data['email']
            name             = data['name']
            password         = data['password']
            request.email    = email
            request.name     = name
            request.password = password
            
            email_pattern    = '^\w+([-_.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$'
            # 8자 이상, 최소 하나의 문자, 숫자, 특수문자
            password_pattern = '^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$'

            if not re.match(email_pattern, email):
                return JsonResponse({'message': 'INVALID EMAIL'}, status = 400)
            if not re.match(password_pattern, password):
                return JsonResponse({'message': 'INVALID PASSWORD'}, status = 400)
            if User.objects.filter(email = email).exists():
                return JsonResponse({'message': 'USER ALREADY EXISTS'}, status=400)

            return func(self, request, *args, **kwargs)
            
        except KeyError as e:
            return JsonResponse({'message': f"{e} FIELD IS MISSING"}, status=400)

    return wrapper