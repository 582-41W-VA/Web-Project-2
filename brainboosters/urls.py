from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("", views.homepage, name="homepage"),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('search/', views.tutor_search, name='tutor_search'),
    path('create-tutor-profile/', views.create_tutor_profile, name='create_tutor_profile'),
    path('create-parent-profile/', views.create_parent_profile, name='create_parent_profile'),
    path('tutor-dashboard/', views.tutor_dashboard, name='tutor_dashboard'),
    path('parent-dashboard/', views.parent_dashboard, name='parent_dashboard'),
    path('tutor/<int:pk>/edit/', views.edit_tutor_profile, name='edit_tutor_profile'),
    path('parent/<int:pk>/edit/', views.edit_parent_profile, name='edit_parent_profile'),
    path('tutors/<int:tutor_id>/', views.tutor_detail, name='tutor_detail'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
