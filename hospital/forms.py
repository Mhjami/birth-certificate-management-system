from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

from .models import Doctor, Hospital, Child


class RegistrationForm(forms.Form):
    hospital = forms.ModelChoiceField(queryset=Hospital.objects.all())
    first_name = forms.CharField(
        required=True, label=_("First Name"), min_length=3, max_length=50
    )
    last_name = forms.CharField(
        required=True, label=_("Last Name"), min_length=3, max_length=50
    )
    email = forms.EmailField(required=True, label=_("Email Address"))
    phone_number = forms.CharField(max_length=15)
    designation = forms.CharField(max_length=20)
    password = forms.CharField(required=True, widget=forms.PasswordInput)

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise ValidationError(_(f"{email} is already registered."))
        return email

    def save(self):
        user = User.objects.create(
            first_name=self.cleaned_data.get("first_name"),
            last_name=self.cleaned_data.get("last_name"),
            email=self.cleaned_data.get("email"),
            username=self.cleaned_data.get("email"),
            is_active=True,
        )
        user.set_password(self.cleaned_data.get("password"))
        user.save()

        doctor = Doctor.objects.create(
            user=user,
            hospital=self.cleaned_data.get("hospital"),
            designation=self.cleaned_data.get("designation"),
            phone_number=self.cleaned_data.get("phone_number"),
        )

        return doctor


class ChildForm(forms.ModelForm):
    class Meta:
        model = Child
        fields = (
            "hospital",
            "first_name",
            "last_name",
            "date_of_birth",
            "blood_group",
            "fathers_name",
            "mothers_name",
            "permanent_address",
            "present_address",
            "city",
        )

    def __init__(self, *args, **kwargs):
        super(ChildForm, self).__init__(*args, **kwargs)
        self.fields['hospital'].widget = forms.HiddenInput()


class NoteForm(forms.Form):
    text = forms.CharField(max_length=5000, required=True, widget=forms.Textarea)
