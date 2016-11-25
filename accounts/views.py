from django.contrib import messages, auth
from accounts.forms import UserRegistrationForm,UserLoginForm
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.template.context_processors import csrf
from django.contrib.auth.decorators import login_required

import arrow
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from models import User
from forms import ContactForm
from django.core.mail import BadHeaderError,send_mail



@login_required(login_url='/login/')
def profile(request):

    return render(request, 'profile.html')



def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()

            user = auth.authenticate(email=request.POST.get('email'),
                                     password=request.POST.get('password1'))

            if user:
                messages.success(request, "You have successfully registered")
                return redirect(reverse('profile'))

            else:
                messages.error(request, "unable to log you in at this time!")

    else:
        form = UserRegistrationForm()

    args = {'form': form}
    args.update(csrf(request))

    return render(request, 'register.html', args)


def login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            user = auth.authenticate(email=request.POST.get('email'),
                                     password=request.POST.get('password'))

            if user is not None:
                auth.login(request, user)
                messages.error(request, "You have successfully logged in")
                return redirect(reverse('profile'))
            else:
                form.add_error(None, "Your email or password was not recognised")

    else:
        form = UserLoginForm()

    args = {'form': form}
    args.update(csrf(request))
    return render(request, 'login.html', args)

def logout(request):
    auth.logout(request)
    messages.success(request, 'You have successfully logged out')
    return redirect(reverse('login'))



def get_contact(request):
   if request.method == 'GET':
       form = ContactForm()
   else:
       form = ContactForm(request.POST)
       if form.is_valid():
           Subject = form.cleaned_data['Subject']
           Email = form.cleaned_data['Email']
           Message = form.cleaned_data['Message']
           try:
               send_mail(Subject, Message, Email, ['testing@example.com'])
           except BadHeaderError:
               return HttpResponse('Invalid header found.')
           return redirect('thanks')
   return render(request, "contact.html", {'form': form})

def thanks(request):
   return render(request, 'thanks.html')