from pyexpat.errors import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render , redirect , reverse
from django.http import HttpResponse
from django.contrib.auth import authenticate , login as auth_login , logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.urls import reverse_lazy
from .forms import RegsiterForm , LoginForm , ForgetPassForm , VerifyOtpForm , ResetPassword , ProfileForm
import random

@login_required(login_url=reverse_lazy('user:login'))
def Home(request):
    return  render(request , 'home.html')

def register(request):
    if request.method == 'POST':
        form = RegsiterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = User.objects.create_user(username = username , password = password , email = email)
            auth_login(request , user)
            return redirect('user:Home')
    else:
        form = RegsiterForm()
    return render(request , 'register.html', {'form':form})


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            try:
                user = User.objects.get(email = email)
            except ObjectDoesNotExist:
                return HttpResponse('invalid email')

            user = authenticate(request , username = user.username , password = password)
            if user is not None:
                auth_login(request , user)
                return redirect('user:Home')
            else:
                return  HttpResponse('invalid password')
    else:
        form = LoginForm()

    return render(request , 'login.html', {'form':form})

def logout(request):
    auth_logout(request)
    return redirect('user:login')



def forgetPass(request):
    if request.method == 'POST':
        form = ForgetPassForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            try:
                user = User.objects.get(email=email)
                otp = random.randint(10000, 99999)

                send_mail(
                    'Your Password Reset',
                    f'Your OTP is {otp}',
                    'marwanpentester@gmail.com',
                    [email],
                )

                request.session['otp'] = otp
                request.session['email'] = email

                messages.success(request, 'OTP sent to your email.')
                return redirect('user:verify_otp')
            except ObjectDoesNotExist:
                messages.error(request, 'Email not found.')
    else:
        form = ForgetPassForm()
    return render(request, 'forgetPassword.html', {'form': form})


def verify_otp(request):
    if request.method == 'POST':
        form = VerifyOtpForm(request.POST)
        if form.is_valid():
            otp = form.cleaned_data.get('otp')

            otp_session = request.session.get('otp')
            email = request.session.get('email')

            if otp_session and int(otp) == otp_session:
                messages.success(request, 'The OTP is valid.')
                return redirect('user:resetPassword')
            else:
                messages.error(request, 'The OTP is invalid.')
    else:
        form = VerifyOtpForm()

    return render(request, 'verify_password.html', {'form': form})


def resetPassword(request):
    if request.method == 'POST':
        form = ResetPassword(request.POST)
        if form.is_valid():
            password = form.cleaned_data.get('password')
            confirm_password = form.cleaned_data.get('confirmPassword')

            if password != confirm_password:
                messages.error(request, "The passwords do not match.")
                return redirect('user:resetPassword')

            email = request.session.get('email')

            if email:
                user = User.objects.get(email=email)
                user.set_password(password)
                user.save()

                messages.success(request, 'The password has been reset successfully.')
                return redirect('user:login')
    else:
        form = ResetPassword()
    return render(request, 'reset_pass.html', {'form': form})


@login_required
def profile_view(request):
    # Initialize forms
    form = ProfileForm(instance=request.user)
    password_form = PasswordChangeForm(request.user)

    if request.method == 'POST':
        # Determine which form is submitted
        if 'update_profile' in request.POST:
            form = ProfileForm(request.POST, instance=request.user)
            if form.is_valid():
                form.save()
                return redirect('user:profile_view')  # Redirect after successful profile update

        elif 'change_password' in request.POST:
            password_form = PasswordChangeForm(request.user, request.POST)
            if password_form.is_valid():
                password_form.save()
                update_session_auth_hash(request, password_form.user)  # Prevent logout
                return redirect('user:profile_view')  # Redirect after successful password change

    context = {
        'form': form,
        'password_form': password_form,
    }
    return render(request, 'profile.html', context)

def get_start(request):
    return redirect('task:Home')