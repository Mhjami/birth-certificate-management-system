from django.urls import path

from hospital.views import get_child_list, add_child, edit_child,view_child
from website import views as website_views

app_name = "website"
urlpatterns = [
    path("", website_views.landing_page, name="landing_page"),
    path("child/", get_child_list, name="child_list"),
    path("child/add/", add_child, name="add_child"),

    path("child/<child_id>/edit/", edit_child, name="edit_child"),
    path("child/<child_id>/", view_child, name="view_child"),
]
