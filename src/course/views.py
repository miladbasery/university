from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Course, StudentProgress
from django.db.models import Q
from collections import defaultdict

@login_required
def dashboard_view(request):
    # دریافت یا ساخت کارنامه دانشجو
    progress, created = StudentProgress.objects.get_or_create(user=request.user)
    
    # --- بخش POST (پردازش فرم‌ها) ---
    if request.method == 'POST':
        
        # 1. پردازش انتخاب اولیه (پاپ‌آپ خوش‌آمدگویی) - [بخش جدید]
        if 'setup_choice' in request.POST:
            choice = request.POST.get('setup_choice')
            
            if choice == 'computer':
                progress.use_default_chart = True  # استفاده از چارت کامپیوتر
            elif choice == 'custom':
                progress.use_default_chart = False # چارت خالی
            
            progress.is_setup_complete = True # تنظیمات اولیه انجام شد
            progress.save()
            return redirect('dashboard')

        # 2. افزودن درس شخصی
        elif 'add_custom_course' in request.POST:
            try:
                new_course = Course.objects.create(
                    creator=request.user,
                    name=request.POST.get('course_name'),
                    units=int(request.POST.get('course_units')),
                    semester=int(request.POST.get('course_semester')),
                    code=f"cust_{request.user.id}_{request.POST.get('course_name')}"
                )
                
                # افزودن پیش‌نیاز
                prereq_id = request.POST.get('course_prereq')
                if prereq_id and prereq_id != "none":
                    try:
                        prereq_course = Course.objects.get(id=prereq_id)
                        new_course.prerequisites.add(prereq_course)
                    except Course.DoesNotExist:
                        pass
            except ValueError:
                pass # هندل کردن خطای احتمالی ورودی
            return redirect('dashboard')
            
        # 3. ذخیره تیک‌ها (لیست درس‌های پاس شده)
        elif 'save_changes' in request.POST:
            selected_course_ids = request.POST.getlist('passed_courses')
            progress.passed_courses.set(selected_course_ids)
            progress.save()
            return redirect('dashboard')

        # 4. حذف درس شخصی
        elif 'delete_course' in request.POST:
            course_id = request.POST.get('course_id')
            try:
                # فقط درسی رو پاک کن که ID اش درسته و سازنده‌اش خودِ کاربره
                course_to_delete = Course.objects.get(id=course_id, creator=request.user)
                course_to_delete.delete()
            except Course.DoesNotExist:
                pass 
            return redirect('dashboard')

    # --- بخش GET (نمایش اطلاعات) ---

    # منطق فیلتر کردن درس‌ها بر اساس انتخاب کاربر [بخش جدید]
    if progress.use_default_chart:
        # اگر چارت پیش‌فرض را خواسته: (درس‌های عمومی) + (درس‌های شخصی خودم)
        courses_query = Q(creator__isnull=True) | Q(creator=request.user)
    else:
        # اگر چارت خالی خواسته: فقط (درس‌های شخصی خودم)
        courses_query = Q(creator=request.user)

    # گرفتن لیست درس‌ها با فیلتر بالا
    all_courses = Course.objects.filter(courses_query).order_by('semester', 'name')
    
    passed_courses = set(progress.passed_courses.all())

    # گروه‌بندی دروس بر اساس ترم
    courses_by_semester = defaultdict(list)
    for course in all_courses:
        courses_by_semester[course.semester].append(course)
    
    sorted_semesters = sorted(courses_by_semester.items())

    # الگوریتم پیشنهاد درس
    suggested_candidates = []
    for course in all_courses:
        # شرط ۱: درس پاس نشده باشد
        if course not in passed_courses:
            # شرط ۲: تمام پیش‌نیازها پاس شده باشند
            prereqs = set(course.prerequisites.all())
            if prereqs.issubset(passed_courses):
                suggested_candidates.append(course)
    
    suggested_candidates.sort(key=lambda x: x.semester)

    # محدودیت ۲۰ واحد
    final_suggestions = []
    total_units = 0
    for course in suggested_candidates:
        if total_units + course.units <= 20:
            final_suggestions.append(course)
            total_units += course.units
        if total_units >= 20: break

    # آیا پاپ‌آپ خوش‌آمدگویی نمایش داده شود؟ [بخش جدید]
    show_setup_modal = not progress.is_setup_complete

    context = {
        'user': request.user,
        'semester_data': sorted_semesters,
        'passed_courses': passed_courses,
        'suggested_courses': final_suggestions,
        'total_units': total_units,
        'all_courses_list': all_courses, # برای لیست کشویی مودال افزودن درس
        'show_setup_modal': show_setup_modal, # برای نمایش پاپ‌آپ اولیه
    }
    return render(request, 'course/dashboard.html', context)