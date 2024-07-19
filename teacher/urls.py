from django.urls import path
from .views import *

urlpatterns = [
    path('', group_list, name='group_list'),
    path('group/add/', add_group, name='add_group'),
    path('group/<int:group_id>/', group_detail, name='group_detail'),
    path('add-student/', add_student, name='add_student'),

    #Update
    path('update-group/<int:pk>/', update_group, name='update_group'),
    path('student/update/<int:pk>/<int:group_id>/', update_student, name='update_student'),

    # Delete
    path('delete-group/<int:pk>/', delete_group, name='delete_group'),
    path('delete-student/<int:pk>/', delete_student, name='delete_student'),

    # Account
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
]
