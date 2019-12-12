from django.db import models
from django.contrib.auth.models import User


class Hospital(models.Model):
    name = models.CharField(max_length=50, unique=True)
    logo = models.ImageField(upload_to="hospital_images/")
    phone_number = models.CharField(max_length=14)
    address = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Doctor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=14)
    profile_picture = models.ImageField(upload_to="doctor_picture/", null=True, blank=True)
    designation = models.CharField(max_length=20)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.get_full_name()


class Note(models.Model):
    created_by = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    text = models.TextField(max_length=10000)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text


class Child(models.Model):
    BLOOD_GROUP_CHOICES = (
        ("A+", "A Positive"),
        ("A-", "A Negative"),
        ("AB+", "AB Positive"),
        ("AB-", "AB Negative"),

    )
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    date_of_birth = models.DateField()
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUP_CHOICES)
    fathers_name = models.CharField(max_length=50)
    mothers_name = models.CharField(max_length=50)
    permanent_address = models.TextField(max_length=600)
    present_address = models.TextField(max_length=600)
    city = models.CharField(max_length=40)
    notes = models.ManyToManyField(Note, blank=True)

    def __str__(self):
        return self.first_name + " " + self.last_name
