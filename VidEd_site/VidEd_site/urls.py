"""
URL configuration for VidEd_site project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from testapp1.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index_page),
    path('reg/', reg_page),
    path('index/', index_page),
    path('auth/login/', login_page),
    path('profile/logout/', logout_page),
    path('profile/', profile_page),
    path('messanger/', messanger_page),
    path('userlist/', userlist_page),
    path('Design/', Design_page),
    path('login/', login_page),
    path('Prog/', Prog_page),
    path('VidEd/', VidEd_page),
    path('check_login/', check_login),
    path('singin/', signin),
    path('neworder/', neworder),
    path('upload/', upload_files),
    path('removeload/', remove_files),
    path('loadneworder/', create_order),
    path('worker/', worker_page),
    path('Orders/', orders_page),
    path('incorrectacc/', incorrent_acc),
    path('worker/logout/', logout_page),
    path('worker/settings/', wsettings_page),
    path('worker/saveskills/', save_skills),
    path('uploadAvatar/', upload_avatar),
    path('profile/settings/', csettings_page),
    path('History/', history_page),
    path('contacts/', contacts_page),
    path('help/', help_page),
    path('new_help/', new_help),
    path('profile/changetg/', change_telegram),
    path('admin_panel/', admin_page),
    path('admin_panel/sales/', sales_page),
    path('order/', order_page),
    path('editinformationorder/', edit_order),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
