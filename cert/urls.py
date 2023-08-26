from django.urls import path, include
from .views import home, add_wait_block, teacher_sign, teacher_delete_wait_block, delete_cert_in_blockchain, get_cert

app_name = 'cert_app'

urlpatterns = [
    path('', home, name="home"),
    path('add-wait-block/', add_wait_block, name="add-wait-block"),
    path('teacher-sign/<str:pk>', teacher_sign, name="teacher-sign"),
    path('teacher-delete-wait-block/<str:pk>', teacher_delete_wait_block, name="teacher-delete-wait-block"),
    path('delete-cert/<int:pk>', delete_cert_in_blockchain, name="delete-cert"),
    path('cert/<int:pk>', get_cert, name="get-cert"),
]
