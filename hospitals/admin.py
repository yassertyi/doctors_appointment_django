from django.contrib import admin
from django.utils.html import format_html
from django.contrib.auth import get_user_model

from hospitals.notification import Notification
from .models import Hospital, HospitalAccountRequest, City, PhoneNumber, HospitalUpdateRequest

User = get_user_model()

@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'status')
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ('status',)
    search_fields = ('name', 'slug')

@admin.register(HospitalAccountRequest)
class HospitalAccountRequestAdmin(admin.ModelAdmin):
    list_display = ['hospital_name', 'manager_full_name', 'logo_display', 'manager_email', 'status', 'created_at', 'view_documents']
    list_filter = ['status', 'created_at']
    search_fields = ['hospital_name', 'manager_full_name', 'manager_email']
    readonly_fields = ['created_at', 'created_by']
    actions = ['approve_requests', 'reject_requests']

    # دالة لعرض الشعار
    def logo_display(self, obj):
        if hasattr(obj, 'hospital') and obj.hospital:  # Check if 'hospital' exists and is not None
            hospital = obj.hospital
            if hospital.logo:
                return format_html('<img src="{}" style="width: 50px; height: auto;" />', hospital.logo.url)
        return "لا يوجد شعار"


    # دالة لعرض المستندات
    def view_documents(self, obj):
        links = []
        if obj.commercial_record:
            links.append(format_html('<a href="{}" target="_blank">السجل التجاري</a>', obj.commercial_record.url))
        if obj.medical_license:
            links.append(format_html('<a href="{}" target="_blank">الترخيص الطبي</a>', obj.medical_license.url))
        return format_html(' | '.join(links))
    view_documents.short_description = 'المستندات'

    # دالة للموافقة على الطلبات
    def approve_requests(self, request, queryset):
        from django.utils import timezone
        from django.utils.text import slugify

        for hospital_request in queryset.filter(status='pending'):
            # إنشاء حساب مستخدم جديد لمدير المستشفى
            user = User.objects.create_user(
                username=hospital_request.manager_email,  # استخدام البريد الإلكتروني كاسم مستخدم
                email=hospital_request.manager_email,
                first_name=hospital_request.manager_full_name.split(' ')[0],
                last_name=' '.join(hospital_request.manager_full_name.split(' ')[1:]),
                user_type='hospital_manager',
                mobile_number=hospital_request.manager_phone,
            )
            user.set_password(hospital_request.manager_password)
            user.save()

            # إنشاء سجل المستشفى
            hospital_slug = slugify(hospital_request.hospital_name)
            # التحقق من وجود slug مشابه وإضافة رقم تسلسلي إذا لزم الأمر
            original_slug = hospital_slug
            counter = 1
            while Hospital.objects.filter(slug=hospital_slug).exists():
                hospital_slug = f"{original_slug}-{counter}"
                counter += 1

            # إنشاء سجل المستشفى
            hospital = Hospital.objects.create(
                user=user,  # ربط المستشفى بالمستخدم
                name=hospital_request.hospital_name,
                slug=hospital_slug,  # الرابط المختصر للمستشفى
                logo=hospital_request.logo,
                description=hospital_request.notes,
                commercial_record=hospital_request.commercial_record,
                medical_license=hospital_request.medical_license,
                created_by=request.user,
                created_at=timezone.now()
            )

            # تحديث حالة الطلب
            hospital_request.status = 'approved'
            hospital_request.reviewed_by = request.user
            hospital_request.reviewed_at = timezone.now()
            hospital_request.save()

           
            try:
                print(f"محاولة إرسال بريد إلكتروني إلى {user.email}")
                email_sent = Notification.send_hospital_manager_credentials(user,hospital_request.hospital_name)
                if not email_sent:
                    print(f"فشل في إرسال البريد الإلكتروني إلى {user.email}")
            except Exception as e:
                self.message_user(request, f"تم إنشاء الحساب ولكن فشل إرسال البريد الإلكتروني: {str(e)}")

        self.message_user(request, f"تمت الموافقة على {queryset.count()} طلب/طلبات بنجاح")
    approve_requests.short_description = "الموافقة على الطلبات المحددة"

    # دالة لرفض الطلبات
    def reject_requests(self, request, queryset):
        queryset.filter(status='pending').update(
            status='rejected',
            reviewed_by=request.user
        )
        self.message_user(request, f"تم رفض {queryset.count()} طلب/طلبات")
    reject_requests.short_description = "رفض الطلبات المحددة"

@admin.register(HospitalUpdateRequest)
class HospitalUpdateRequestAdmin(admin.ModelAdmin):
    list_display = ['hospital', 'name', 'location', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['hospital__name', 'name', 'location']
    readonly_fields = ['created_at', 'created_by', 'hospital']
    actions = ['approve_requests', 'reject_requests']

    # دالة للموافقة على الطلبات
    def approve_requests(self, request, queryset):
        for update_request in queryset.filter(status='pending'):
            update_request.approve_request(request.user)

        self.message_user(request, f"تمت الموافقة على {queryset.count()} طلب/طلبات بنجاح")
    approve_requests.short_description = "الموافقة على الطلبات المحددة"

    # دالة لرفض الطلبات
    def reject_requests(self, request, queryset):
        queryset.filter(status='pending').update(
            status='rejected',
            reviewed_by=request.user
        )
        self.message_user(request, f"تم رفض {queryset.count()} طلب/طلبات")
    reject_requests.short_description = "رفض الطلبات المحددة"

# تسجيل النماذج في واجهة الإدارة
admin.site.register(Hospital)
admin.site.register(PhoneNumber)