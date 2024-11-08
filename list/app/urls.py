from django.urls import path
from . import views

urlpatterns = [
    path('',views.login_view,name="login"),
    path('signup',views.signup_view,name="signup"),
    path('logout/',views.logout_view,name="logout"),
    path('index/',views.index,name="index"),
    path('edit_item/<int:list_id>',views.edit_item,name="edit_item"),
    path('del_item/<int:list_id>',views.del_item,name="del_item"),
    path('add_item/',views.add_item,name="add_item"),
]