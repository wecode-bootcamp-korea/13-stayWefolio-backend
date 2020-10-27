import json
import bcrypt
import jwt
import re

from django.views     import View
from django.shortcuts import get_object_or_404
from django.http      import JsonResponse

from .models          import User
from my_settings      import SECRET_KEY, ALGORITHM
from .utils           import signup_validator

class SignUpView(View):
    @signup_validator
    def post(self, request):
        hashed_password  = bcrypt.hashpw(request.password.encode('utf-8'), bcrypt.gensalt())
        decoded_password = hashed_password.decode('utf-8')

        User(
            email    = request.email,
            name     = request.name,
            password = decoded_password
        ).save()

        return JsonResponse({'message': 'SUCCESS'}, status=201)

class LoginView(View):
    def post(self, request):
        try:
            data     = json.loads(request.body)
            email    = data['email']
            password = data['password']
            user     = User.objects.get(email=email)

            if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                access_token  = jwt.encode({'user_id':user.id}, SECRET_KEY, algorithm=ALGORITHM)
                decoded_token = access_token.decode('utf-8')
                return JsonResponse({'TOKEN': decoded_token}, status=200)

            return JsonResponse({'message': 'WRONG PASSWORD'}) 

        except KeyError as e:
            return JsonResponse({'message': f"{e} FIELD IS MISSING"}, status=400)

        except User.DoesNotExist:
            return JsonResponse({'message': 'USER DOES NOT EXIST'}, status=400)