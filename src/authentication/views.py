from django.shortcuts import render, redirect
from django.contrib.auth import login, logout , update_session_auth_hash
from .forms import StudentSignUpForm, StudentLoginForm , ProfileUpdateForm
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required


def signup_view(request):
    if request.method == 'POST':
        form = StudentSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            # بعد از ثبت‌نام، بلافاصله لاگین شود
            login(request, user)
            return redirect('dashboard') # فرض بر این است که نام صفحه اصلی dashboard است
    else:
        form = StudentSignUpForm()
    return render(request, 'authentication/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = StudentLoginForm(data=request.POST)
        if form.is_valid():
            # متد get_user کاربر احراز هویت شده را برمی‌گرداند
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = StudentLoginForm()
    return render(request, 'authentication/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def profile_view(request):
    user = request.user

    if request.method == 'POST':
        
        if 'update_info' in request.POST:
            # نکته مهم: request.FILES برای دریافت فایل الزامی است
            info_form = ProfileUpdateForm(request.POST, request.FILES, instance=user)
            password_form = PasswordChangeForm(user)
            
            if info_form.is_valid():
                info_form.save()
                messages.success(request, 'اطلاعات با موفقیت بروزرسانی شد.')
                return redirect('profile')
            
        # ۲. بررسی دکمه تغییر رمز عبور
        elif 'change_password' in request.POST:
            password_form = PasswordChangeForm(user, request.POST)
            info_form = ProfileUpdateForm(instance=user) # فرم اطلاعات پر باشد ولی پردازش نشود
            
            if password_form.is_valid():
                user = password_form.save()
                # این خط خیلی مهم است: جلوگیری از لاگ‌اوت شدن کاربر
                update_session_auth_hash(request, user)
                messages.success(request, 'رمز عبور شما با موفقیت تغییر کرد.')
                return redirect('profile')
            else:
                messages.error(request, 'لطفاً خطاهای مربوط به رمز عبور را رفع کنید.')

    else:
        # حالت GET: نمایش فرم‌های پر شده با اطلاعات فعلی
        info_form = ProfileUpdateForm(instance=user)
        password_form = PasswordChangeForm(user)

    return render(request, 'authentication/profile.html', {
        'info_form': info_form,
        'password_form': password_form
    })