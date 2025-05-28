from django import template
from bookings.models import Booking

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """
    فلتر للوصول إلى عناصر القاموس باستخدام المفتاح
    مثال: {{ my_dict|get_item:key_var }}
    """
    return dictionary.get(key)

@register.filter
def count_bookings(patient, hospital_id=None):
    """
    فلتر لحساب عدد الحجوزات المؤكدة لمريض معين
    مثال: {{ patient|count_bookings:hospital.id }}
    """
    try:
        # إنشاء استعلام أساسي للحجوزات المؤكدة فقط
        query = Booking.objects.filter(patient=patient, status='confirmed')
        
        # إذا تم تمرير معرف المستشفى، نحسب الحجوزات لهذه المستشفى فقط
        if hospital_id:
            query = query.filter(hospital_id=hospital_id)
            
        # حساب عدد الحجوزات المؤكدة
        return query.count()
    except Exception as e:
        print(f"Error counting confirmed bookings: {e}")
        return 0

@register.filter
def count_pending_bookings(patient, hospital_id=None):
    """
    فلتر لحساب عدد الحجوزات قيد الانتظار لمريض معين
    مثال: {{ patient|count_pending_bookings:hospital.id }}
    """
    try:
        # إنشاء استعلام أساسي للحجوزات قيد الانتظار فقط
        query = Booking.objects.filter(patient=patient, status='pending')
        
        # إذا تم تمرير معرف المستشفى، نحسب الحجوزات لهذه المستشفى فقط
        if hospital_id:
            query = query.filter(hospital_id=hospital_id)
            
        # حساب عدد الحجوزات قيد الانتظار
        return query.count()
    except Exception as e:
        print(f"Error counting pending bookings: {e}")
        return 0

@register.filter
def count_cancelled_bookings(patient, hospital_id=None):
    """
    فلتر لحساب عدد الحجوزات الملغاة لمريض معين
    مثال: {{ patient|count_cancelled_bookings:hospital.id }}
    """
    try:
        # إنشاء استعلام أساسي للحجوزات الملغاة فقط
        query = Booking.objects.filter(patient=patient, status='cancelled')
        
        # إذا تم تمرير معرف المستشفى، نحسب الحجوزات لهذه المستشفى فقط
        if hospital_id:
            query = query.filter(hospital_id=hospital_id)
            
        # حساب عدد الحجوزات الملغاة
        return query.count()
    except Exception as e:
        print(f"Error counting cancelled bookings: {e}")
        return 0
