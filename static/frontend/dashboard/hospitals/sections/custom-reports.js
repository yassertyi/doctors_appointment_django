// كود JavaScript خاص للتعامل مع أزرار التقارير
$(document).ready(function() {
  // إضافة معالج نقر لزر تقارير الأطباء
  $("[data-method='doctor_reports']").click(function(e) {
    e.preventDefault();
    
    // إخفاء جميع الأقسام
    $(".section").addClass("d-none");
    
    // إظهار قسم تقارير الأطباء
    $(".doctor_reports.section").removeClass("d-none");
    
    // تغيير عنوان الصفحة إذا كانت الدالة متاحة
    if (typeof updateBreadcrumb === 'function') {
      updateBreadcrumb("تقارير الأطباء");
    }
    
    // إضافة حالة نشطة لزر القائمة
    $(".dashboard-menu li").removeClass("active");
    $(".dashboard-menu li a[data-method='reports_dashboard']").parent().addClass("active");
    
    console.log("تم النقر على تقارير الأطباء");
  });
});
