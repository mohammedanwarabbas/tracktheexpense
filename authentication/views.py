from django.contrib import auth
from django.shortcuts import render
from django.views import View
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from email_validator import validate_email, EmailNotValidError
from django.contrib import messages
from django.core.mail import EmailMessage
from django.shortcuts import redirect

#from django import reverse
from django.urls import reverse
# path to view
#from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
#NOTE force_text has been changed into force_str in new django version
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from .utils import token_generator


class UsernameValidation(View):
    def post(self,request):
        data = json.loads(request.body)
        username = data["username"]

        if not str(username).isalnum():
            return JsonResponse({"username_error":'Username should contain alphanumeric charecter'},status=400)

        if User.objects.all().filter(username=username).exists():
            return JsonResponse({"username_error":'Username already taken'},status=409)
               
        return JsonResponse({"username_valid":True})


class EmailValidation(View):
    def post(self,request):
        data = json.loads(request.body)
        email = data['email']



        try:
            # Validate.
            valid = validate_email(email)
            # Update with the normalized form.
            #email = valid.email
            if User.objects.all().filter(email=email).exists():
                return JsonResponse({"email_error":'Email was already taken'},status=409)
        except EmailNotValidError as e:
            # email is not valid, exception message is human-readable
            #print(str(e))
            return JsonResponse({"email_error":"Email is invalid"},status=400)
        else:
            return JsonResponse({"email_valid":True})

        
            



class RegistrationView(View):
    def get(self,request):
        return render(request, 'authentication/register.html')

    def post(self, request):
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        context = {
            'fieldValue' : request.POST
        }

        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():
                if len(password)<8:
                   messages.error(request,"Password charecters is less than 8") 
                   return render(request, 'authentication/register.html', context)
                
                user = User.objects.create_user(username=username, email=email)
                user.set_password(password)
                user.is_active = False
                user.save()

                #pip install six
                # path to view
                # - getting domain we are on
                # - relative url to verification

                #constructing domain
                domain = get_current_site(request).domain
                uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
                link = reverse('activate',kwargs={'uidb64':uidb64,'token':token_generator.make_token(user)})
                email_subject='This is email_subject'
                activate_url='http://'+domain+link
                email_body = "Hey"+user.username + "Please use this link to verify ur account\n" + activate_url
                email = EmailMessage(
                    email_subject,
                    email_body,
                    'from@example.com',
                    [email],
                )
                email.send(fail_silently=False)
                messages.success(request,"Registration done successfully") 
                return render(request, 'authentication/register.html')

        return render(request, 'authentication/register.html')

class VerificationView(View):
    def get(self, request, uidb64 ,token):
        try:
            id=force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=id)
            if not token_generator.check_token(user, token):
                return redirect('login'+'?message=user already activated')

            if user.is_active:
                redirect('login')
            user.is_active = True
            user.save()
            messages.success(request, 'Your account activated successfully')
            return redirect('login')
        except Exception as e:
            messages.error(request,e)

        return redirect('login')

class LoginView(View):
    def get(self, request):
        return render(request, 'authentication/login.html')

    def post(self, request):
        user_name = request.POST['username']
        password = request.POST['password']
        if user_name and password:
            user = auth.authenticate(username=user_name, password=password)
            if user:
                if user.is_active:
                    auth.login(request, user)
                    messages.success(request, 'Welcome'+user.username+' you are now logged in')
                    return redirect('expenses')
                
                messages.error(request, user.username+' You should activate u r account! Check your email for the link')
                return render(request, 'authentication/login.html')
            messages.error(request, 'Invalid credentials')  
            return render(request,'authentication/login.html')
        messages.error(request, 'Please enter username and password')
        return render(request, 'authentication/login.html')

class LogoutView(View):
    def post(self, request):
        auth.logout(request)
        messages.success(request, 'You have been Logged out')
        return redirect('login')