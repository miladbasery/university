from django.db import models
from django.conf import settings

class Course(models.Model):
    # فیلد جدید: صاحب درس (اگر null باشد یعنی عمومی است)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, related_name='created_courses')
    
    name = models.CharField(max_length=100, verbose_name="نام درس")
    # کد درس رو دیگه unique نمذاریم چون ممکنه دو نفر یه درس با کد ۱ بسازن
    code = models.CharField(max_length=20, verbose_name="کد درس") 
    units = models.PositiveIntegerField(default=3, verbose_name="تعداد واحد")
    semester = models.PositiveIntegerField(verbose_name="ترم")
    
    prerequisites = models.ManyToManyField('self', symmetrical=False, blank=True, related_name='required_for', verbose_name="پیش‌نیازها")

    def __str__(self):
        type_str = "شخصی" if self.creator else "عمومی"
        return f"{self.name} ({type_str})"
    
class StudentProgress(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='progress')
    passed_courses = models.ManyToManyField(Course, blank=True, related_name='passed_by_students', verbose_name="دروس پاس شده")
    
    # فیلدهای جدید برای تنظیمات اولیه
    is_setup_complete = models.BooleanField(default=False, verbose_name="تکمیل تنظیمات اولیه")
    use_default_chart = models.BooleanField(default=True, verbose_name="استفاده از چارت پیش‌فرض")

    def __str__(self):
        return f"کارنامه {self.user.username}"