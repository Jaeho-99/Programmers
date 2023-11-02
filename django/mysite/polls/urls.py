from django.urls import path
from . import views

# 해당 앱의 이름 설정.
app_name = 'polls'
urlpatterns = [
	path('', views.index, name='index'),
    path('<int:question_id>/', views.detail, name='detail'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    path('<int:question_id>/result', views.result, name='result'),
]