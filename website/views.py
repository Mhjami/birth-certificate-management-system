from django.shortcuts import redirect


def landing_page(request):
    if request.user.is_authenticated:
        return redirect("/child/")
    else:
        return redirect("/user/login/")

