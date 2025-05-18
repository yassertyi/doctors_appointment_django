from social_core.pipeline.partial import partial
from patients.models import Patients
from django.utils import timezone
from datetime import date
import requests
from django.core.files.base import ContentFile

@partial
def create_patient_profile(backend, user, response, *args, **kwargs):
    """
    Set user type as patient and create patient record for users who sign up using Google OAuth2
    """
    if backend.name == 'google-oauth2':
        # تحديث بيانات المستخدم من Google
        user_updated = False
        
        if not user.first_name and 'given_name' in response:
            user.first_name = response['given_name']
            user_updated = True
            
        if not user.last_name and 'family_name' in response:
            user.last_name = response['family_name']
            user_updated = True
            
        if not user.email and 'email' in response:
            user.email = response['email']
            user_updated = True
            
        # تحميل صورة المستخدم من Google
        if not user.profile_picture and 'picture' in response:
            try:
                picture_response = requests.get(response['picture'])
                if picture_response.status_code == 200:
                    # تحميل الصورة وحفظها
                    filename = f'google_profile_{user.id}.jpg'
                    user.profile_picture.save(
                        filename,
                        ContentFile(picture_response.content),
                        save=False
                    )
                    user_updated = True
            except Exception as e:
                print(f'Error downloading profile picture: {e}')
            
        # Set user type as patient if not set
        if not user.user_type:
            user.user_type = 'patient'
            user_updated = True
            # Set mobile number to a default value temporarily
            if not user.mobile_number:
                user.mobile_number = 'pending_update'
                user_updated = True
                
        if user_updated:
            user.save()
            
        # التحقق من وجود سجل المريض
        try:
            # محاولة الحصول على سجل المريض الحالي
            patient = Patients.objects.get(user=user)
            # تحديث الملاحظات فقط إذا كانت فارغة
            if not patient.notes:
                user_full_name = f"{user.first_name} {user.last_name}".strip()
                notes = f'تم تسجيل الدخول بواسطة {user_full_name} عبر Google'
                patient.notes = notes
                patient.save(update_fields=['notes', 'updated_at'])
        except Patients.DoesNotExist:
            # إنشاء سجل جديد فقط إذا لم يكن موجوداً
            default_birth_date = date(2000, 1, 1)
            user_full_name = f"{user.first_name} {user.last_name}".strip()
            notes = f'تم إنشاء الحساب لـ {user_full_name} عبر Google - يرجى تحديث البيانات الشخصية'
            
            patient = Patients.objects.create(
                user=user,
                birth_date=default_birth_date,
                gender='Male',
                notes=notes,
                created_at=timezone.now(),
                updated_at=timezone.now()
            )
