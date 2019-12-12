from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View

from .forms import RegistrationForm, ChildForm, NoteForm
from .models import Hospital, Child, Doctor


def list_hospital(request):
    hospitals = Hospital.objects.filter(name__icontains="Jami" "" "")
    return render(request, "hospital/hospital-list.html", {"hospitals": hospitals})


class DoctorRegistrationView(View):
    form_class = RegistrationForm
    template_name = "hospital/sign-up.html"

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            doctor = form.save()
            login(request, doctor.user)
            return redirect("/")

        return render(request, self.template_name, {"form": form})


def get_child_list(request):
    if request.user.is_authenticated is False:
        return redirect("/user/login")

    doctor = Doctor.objects.get(user=request.user)

    search = request.GET.get("search", None)

    if search is not None:
        childs = Child.objects.filter(hospital=doctor.hospital, first_name__icontains=search)
    else:
        childs = Child.objects.filter(hospital=doctor.hospital)

    return render(request, "hospital/child-list.html", {"childs": childs})


@login_required()
def add_child(request):
    if request.method == "POST":
        form = ChildForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/child/")
        else:
            return render(request, "hospital/add-child.html", {"form": form})
    else:
        hospital = Doctor.objects.get(user=request.user).hospital
        form = ChildForm(initial={"hospital": hospital.id})
        return render(request, "hospital/add-child.html", {"form": form})


@login_required()
def view_child(request, child_id):
    child = get_object_or_404(Child, id=child_id)
    if request.method == "POST":
        form = NoteForm(request.POST)
        doctor = get_object_or_404(Doctor, user=request.user)
        if form.is_valid():
            child.notes.create(created_by=doctor, text=form.cleaned_data.get("text"))
            return redirect(f"/child/{child.id}/")
        else:
            return render(request, "hospital/view.html", {"child": child, "form": form})
    form = NoteForm()
    return render(request, "hospital/view.html", {"child": child, "form": form})


@login_required()
def edit_child(request, child_id):
    child = get_object_or_404(Child, id=child_id)
    if request.method == "POST":
        form = ChildForm(request.POST, instance=child)
        if form.is_valid():
            form.save()
            return redirect("/child/")
        else:
            return render(request, "hospital/add-child.html", {"form": form})
    else:

        form = ChildForm(
            initial={
                "hospital": child.hospital.id,
                "first_name": child.first_name,
                "last_name": child.last_name,
                "date_of_birth": child.date_of_birth,
                "blood_group": child.blood_group,
                "fathers_name": child.fathers_name,
                "mothers_name": child.mothers_name,
                "permanent_address": child.permanent_address,
                "present_address": child.present_address,
                "city": child.city,
            }
        )
        return render(request, "hospital/add-child.html", {"form": form})
