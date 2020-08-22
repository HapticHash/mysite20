from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from myapp import views

app_name = 'myapp'

urlpatterns = [
 path(r'', views.index, name='index'),
 path(r'about', views.about, name='about'),
 path(r'<int:top_no>', views.detail, name='detail'),
 path(r'courses',views.courses, name='courses'),
 path(r'place_order', views.place_order, name='placeorder'),
 path(r'courses/<int:cour_id>', views.coursedetail, name='coursedetail'),
 path(r'login', views.user_login, name='login'),
 path(r'logout', views.user_logout, name='logout'),
 path(r'myaccount', views.myaccount, name='myaccount'),
 path(r'register', views.register, name='register'),
 path(r'forgotpassword', views.forgot_password, name='forgot_password'),
 path(r'feedback', views.feedback, name='feedback')
]