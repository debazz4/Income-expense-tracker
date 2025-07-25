from django.shortcuts import render, redirect
from django.views import View
from django.http import JsonResponse
from django.contrib.auth.models import User
from .models import ActivationEmail
import json
from validate_email import validate_email
from django.contrib import messages
from django.core.mail import EmailMessage, send_mail
from django.conf import settings
from django.http import HttpResponse
from django.urls import reverse
from django.utils.encoding import force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from .utils import token_generator
EMAIL_HOST_USER = settings.EMAIL_HOST_USER


class UsernameValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data['username']

        if not str(username). isalnum():
            return JsonResponse({'username_error': 'username should only contain alphanueric characters.'}, status=400)
        if User.objects.filter(username=username).exists():
            return JsonResponse({'username_error': 'username already exists.'}, status=409)
        return JsonResponse({'username_valid': True})

class EmailValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        email = data['email']

        if not validate_email(email):
            return JsonResponse({'email_error': 'Email is invalid.'}, status=400)
        if User.objects.filter(email=email).exists():
            return JsonResponse({'email_error': 'Email already in use.'}, status=409)
        return JsonResponse({'email_valid': True})

class RegistrationView(View):
    def get(self, request):
        return render(request, 'authentication/register.html')

    def post(self, request):
        # Get user data and send email
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        context = {
            'fieldValues': request.POST
        }

        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():
                if len(password)<6:
                    messages.error(request, 'Password is too short!')
                    return render(request, 'authentication/register.html', context)
                
            user = User.objects.create_user(username=username, email=email)
            user.set_password(password)
            user.is_active = False
            user.save()
            
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            
            domain = get_current_site(request).domain
            link = reverse('activate', kwargs={
                'uidb64': uidb64,
                'token': token_generator.make_token(user),
            })

            activate_url = 'http://' + domain + link
            # Send activation email
            email_subject = 'Activate your account'
            email_body = 'Hi ' + user.username + ' Please use this link to verify your account\n' + activate_url
            send_mail(
                subject = email_subject,
                message = email_body,
                from_email = EMAIL_HOST_USER,
                recipient_list = [user.email],
                fail_silently=False,
            )

            email = ActivationEmail()
            email.email = user.email
            email.save()
            

            messages.success(request, 'Account has been successfully created.')
            return render(request, 'authentication/register.html')

        return render(request, 'authentication/register.html')
 
class VerificationView(View):
    def get(self, request, uidb64, token):
        return redirect('login')

