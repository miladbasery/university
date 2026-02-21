from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser

# فرم ثبت‌نام (برای ساخت یوزر جدید)
class StudentSignUpForm(UserCreationForm):
    class Meta:
        model = CustomUser
        # فقط فیلدهایی که در مدل CustomUser تعریف کردیم
        fields = ('username', 'university_name')

# فرم لاگین (برای ورود)
class StudentLoginForm(AuthenticationForm):
    # این فرم نیاز به تغییر خاصی ندارد و از استاندارد جنگو استفاده می‌کند
    # اما باید اینجا باشد تا views.py بتواند آن را ایمپورت کند
    pass

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'university_name', 'avatar'] # آواتار اضافه شد
        help_texts = {
            'username': 'نام کاربری جدید خود را وارد کنید.',
        }

