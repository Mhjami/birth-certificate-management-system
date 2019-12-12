from django.contrib import admin
from .models import Hospital, Doctor, Note, Child

@admin.register(Hospital)
class HospitalAdmin(admin.ModelAdmin):
    date_hierarchy = "created_at"
    list_display = ("id", "name", "phone_number", "created_at")
    search_fields = ("name", "phone_number",)


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ("user", "phone_number", "designation",)
    search_fields = ("phone_number",)
    list_filter = ("designation",)


admin.site.register(Note)


@admin.register(Child)
class ChildAdmin(admin.ModelAdmin):
    date_hierarchy = "date_of_birth"
    list_display = ("first_name", "last_name", "date_of_birth", "blood_group")
    list_filter = ("date_of_birth", "blood_group",)
