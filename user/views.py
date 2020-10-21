import json
import bcrypt
import jwt
import re

from django.views     import View
from django.shortcuts import get_object_or_404
from django.http      import JsonResponse

from .models          import User
from my_settings      import SECRET_KEY, ALGORITHM

class SignUpView(View):
    def post(self, request):
        email_pattern    = '^\w+([-_.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$'
        # 8자 이상, 최소 하나의 문자, 숫자, 특수문자
        password_pattern = '^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$'
        try:
            data     = json.loads(request.body)
            email    = data['email']
            name     = data['name']
            password = data['password']
            
            if re.match(email_pattern, email) == None:
                return JsonResponse({'message': 'INVALID EMAIL'}, status = 400)
            if re.match(password_pattern, password) == None:
                return JsonResponse({'message': 'INVALID PASSWORD'}, status = 400)
            if User.objects.filter(email = email).exists():
                return JsonResponse({'message': 'USER ALREADY EXISTS'})

            hashed_password  = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            decoded_password = hashed_password.decode('utf-8')
            User(
                email    = email,
                name     = name,
                password = decoded_password
            ).save()
            return JsonResponse({'message': 'SUCCESS'}, status=201)
        except KeyError as e:
            return JsonResponse({'message': f"{e} FIELD IS MISSING"}, status=400)

class LoginView(View):
    def post(self, request):
        try:
            data     = json.loads(request.body)
            email    = data['email']
            password = data['password']
            user     = User.objects.get(email=email)

            if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                access_token  = jwt.encode({'user_id':user.id}, SECRET_KEY, algorithms=ALGORITHM)
                decoded_token = access_token.decode('utf-8')
                return JsonResponse({'TOKEN': decoded_token}, status=200)
            return JsonResponse({'message': 'WRONG PASSWORD'}) 
        except KeyError as e:
            return JsonResponse({'message': f"{e} FIELD IS MISSING"}, status=400)
        except User.DoesNotExist:
            return JsonResponse({'message': 'USER DOES NOT EXIST'}, status=400)