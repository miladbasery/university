from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# 1. کلاس مدیریت کاربران (برای اینکه جنگو بفهمه چطور یوزر بسازه)
class CustomUserManager(BaseUserManager):
    def create_user(self, username, university_name, password=None):
        if not username:
            raise ValueError('کاربر باید نام کاربری داشته باشد')
        if not university_name:
            raise ValueError('نام دانشگاه الزامی است')

        user = self.model(
            username=username,
            university_name=university_name,
        )
        
        user.set_password(password) # این خط پسورد را هش (رمزنگاری) می‌کند
        user.save(using=self._db)
        return user

    def create_superuser(self, username, university_name, password=None):
        user = self.create_user(
            username=username,
            university_name=university_name,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

# 2. مدل اصلی یوزر (فقط فیلدهایی که تو میخوای)
class CustomUser(AbstractBaseUser):
    username = models.CharField(max_length=50, unique=True, verbose_name="نام کاربری")
    university_name = models.CharField(max_length=100, verbose_name="نام دانشگاه")
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True, verbose_name="تصویر پروفایل")
    
    # فیلدهای اجباری برای مدیریت سیستم
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = CustomUserManager()

    # فیلدی که به عنوان شناسه اصلی استفاده می‌شود (برای لاگین)
    USERNAME_FIELD = 'username'
    # فیلدهایی که موقع ساخت superuser علاوه بر username و password پرسیده شود
    REQUIRED_FIELDS = ['university_name']

    def __str__(self):
        return self.username

    # این متدها برای دسترسی‌های ادمین پنل لازم هستند
    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin