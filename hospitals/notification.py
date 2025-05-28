from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.translation import gettext as _
import logging

logger = logging.getLogger(__name__)  

class Notification:
    @staticmethod
    def send_hospital_manager_credentials(user, hospital_name):
        """
        إرسال بريد إلكتروني بمعلومات تسجيل الدخول لمدير السمتشفى
        """
        subject = _('معلومات تسجيل الدخول لنظام إدارة الفندق')
        context = {
            'hospital_name': hospital_name,
            'username': user.username,
            'login_url': settings.LOGIN_URL
        }
        
        # إرسال البريد الإلكتروني
        html_message = render_to_string('emails/hospital_manager_credentials.html', context)
        plain_message = f"""مرحباً {user.get_full_name()},

تم قبول طلبك لإدارة فندق {hospital_name}. يمكنك تسجيل الدخول باستخدام المعلومات التالية:

اسم المستخدم: {user.username}

يرجى تغيير كلمة المرور بعد تسجيل الدخول لأول مرة.

مع تحيات،
فريق إدارة الفنادق"""

        try:
            # التحقق من إعدادات البريد الإلكتروني
            if not settings.EMAIL_HOST or not settings.EMAIL_PORT:
                print("خطأ في الإعدادات: لم يتم تكوين خادم البريد الإلكتروني")
                return False

            if not settings.DEFAULT_FROM_EMAIL:
                print("خطأ في الإعدادات: لم يتم تحديد عنوان المرسل")
                return False

            if not user.email:
                print(f"خطأ: لا يوجد بريد إلكتروني للمستخدم {user.username}")
                return False

            # محاولة إرسال البريد الإلكتروني
            send_mail(
                subject=subject,
                message=plain_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                html_message=html_message,
                fail_silently=False
            )
            print(f"تم إرسال البريد الإلكتروني بنجاح إلى {user.email}")
            return True
        except Exception as e:
            print(f"""
خطأ في إرسال البريد الإلكتروني:
- نوع الخطأ: {type(e).__name__}
- رسالة الخطأ: {str(e)}
- المستخدم: {user.username}
- البريد الإلكتروني: {user.email}
- إعدادات البريد:
  * EMAIL_HOST: {getattr(settings, 'EMAIL_HOST', 'غير محدد')}
  * EMAIL_PORT: {getattr(settings, 'EMAIL_PORT', 'غير محدد')}
  * DEFAULT_FROM_EMAIL: {getattr(settings, 'DEFAULT_FROM_EMAIL', 'غير محدد')}
""")
            return False