import json
import bcrypt
import jwt

from django.views import View
from django.shortcuts import get_object_or_404
from django.http import JsonResponse

from .models import User
from my_settings import SECRET_KEY, ALGORITHM

class SignUpView(View):
    def post(self, request):
        try:
            data=json.loads(request.body)
            email=data['email']
            name=data['name']
            password=data['password']
            if '@' not in email or '.' not in email:
                return JsonResponse({'message': 'INVALID EMAIL'}, status=400)
            if len(password)<8:
                return JsonResponse({'message': 'PASSWORD TOO SHORT'}, status=400)

            hashed_password=bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            decoded_password=hashed_password.decode('utf-8')
            User(
                email=email,
                name=name,
                password=decoded_password
            ).save()
            return JsonResponse({'message': 'SUCCESS'}, status=201)
        except KeyError:
            check_list=['email', 'name', 'password']
            for key in check_list:
                if key not in data.keys():
                    key=key.upper()
                    return JsonResponse({'message': f"{key} FIELD IS MISSING"}, status=400)


class LoginView(View):
    def post(self, request):
        try:
            data=json.loads(request.body)
            email=data['email']
            password=data['password']
            user=get_object_or_404(User, email=email)

            if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                access_token=jwt.encode({'user_id':user.id}, SECRET_KEY, algorithm=ALGORITHM)    
                decoded_token=access_token.decode('utf-8')
                return JsonResponse({'TOKEN': decoded_token}, status=200)
            return JsonResponse({'message': 'WRONG PASSWORD'}) 
        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)