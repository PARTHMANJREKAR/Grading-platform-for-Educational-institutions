from django.contrib import admin
from django.urls import path
from myapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.login_view, name='login'),
    path('enter_mse_marks/', views.enter_mse_marks_view, name='enter_mse_marks'),
    path('enter_ese_marks/', views.enter_ese_marks_view, name='enter_ese_marks'),
    path('enter_marks/', views.enter_marks_view, name='enter_marks'),
    path('', views.login_view, name='login_root'),
    path('main_page/', views.main_page_view, name='main_page'),
    path('main_page/select_theory_practical/', views.select_theory_practical_view, name='select_theory_practical'),
    path('main_page_2/', views.main_page_2_view, name='main_page_2'),
    path('theory_marks/<str:prn>/', views.theory_marks_view, name='theory_marks'),
    path('practical_marks/<str:prn>/', views.practical_marks_view, name='practical_marks'),
]