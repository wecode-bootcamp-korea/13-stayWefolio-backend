import json
import bcrypt
import jwt
import re

from django.views     import View
from django.shortcuts import get_object_or_404
from django.http      import JsonResponse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes, force_str
from django.contrib.sites.shortcuts import get_current_site

from .models          import User
from my_settings      import SECRET_KEY, ALGORITHM, EMAIL
from .utils           import signup_validator
from .email           import message

class SignUpView(View):
    @signup_validator
    def post(self, request):
        hashed_password  = bcrypt.hashpw(request.password.encode('utf-8'), bcrypt.gensalt())
        decoded_password = hashed_password.decode('utf-8')
        
        user=User.objects.create(
            email    = request.email,
            name     = request.name,
            password = decoded_password
        )
        current_site    = get_current_site(request)
        domain          = current_site.domain
        uidb64          = urlsafe_base64_encode(force_bytes(user.id))
        token           = jwt.encode({'user_id':user.id}, SECRET_KEY, algorithm=ALGORITHM)
        message_content = message(domain, uidb64, token.decode('utf-8'))
        title           = "Complete your email registration"
        mail_to         = request.email
        email           = EmailMessage(title, message_content, to=[mail_to])
        try:
            email.send()
            return JsonResponse({'message': 'SUCCESS'}, status=201)
        except Exception as e:
            return JsonResponse({'dd':f"{e}"}, status=400)
        
class ActivateView(View):
    def get(self, request, uidb64, token):
        try:
            user_id = force_str(urlsafe_base64_decode(uidb64))
            user    = User.objects.get(id=user_id)
            payload = jwt.decode(token, SECRET_KEY, algorithm=ALGORITHM)
            if user.id == payload['user_id']:
                user.is_active=True
                user.save()
                return JsonResponse({'message':'ACTIVATION SUCCESS'}, status=200)
            return JsonResponse({'message':'ACTIVATION FAILED'}, status=400)
        
        except jwt.DecodeError as e:
            return JsonResponse({'message': f"{e}"}, status=400)
        except KeyError as e:
            return JsonResponse({'message': f"{e} IS MISSING"}, status=400)

class LoginView(View):
    def post(self, request):
        try:
            data     = json.loads(request.body)
            email    = data['email']
            password = data['password']
            user     = User.objects.get(email=email)

            if not user.is_active:
                return JsonResponse({'message': 'ACTIVATE YOUR ACCOUNT FIRST'}, status= 400)

            if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                access_token  = jwt.encode({'user_id':user.id}, SECRET_KEY, algorithm=ALGORITHM)
                decoded_token = access_token.decode('utf-8')
                return JsonResponse({'TOKEN': decoded_token}, status=200)

            return JsonResponse({'message': 'WRONG PASSWORD'}) 

        except KeyError as e:
            return JsonResponse({'message': f"{e} FIELD IS MISSING"}, status=400)

        except User.DoesNotExist:
            return JsonResponse({'message': 'USER DOES NOT EXIST'}, status=400)