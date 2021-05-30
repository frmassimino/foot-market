from django.urls import path
from .views import (UserRegisterView,
    UserOverviewView,
                    LoginView,
                    LogoutView,
                    UserHistoryView
)

app_name = 'user'
urlpatterns = [
    #path('', CourseView.as_view(template_name='contact.html'), name='courses-list'),
    #path('', my_fbv, name='courses-list'),
    #path('<int:id>/', CourseView.as_view(), name='courses-detail'),
    #path('', CourseListView.as_view(), name='courses-list'),
    #path('', MyListView.as_view(), name='courses-list'),
    #path('create/', CourseCreateView.as_view(), name='courses-create'),
    #path('<int:id>/update/', CourseUpdateView.as_view(), name='courses-update'),
    #path('<int:id>/delete/', CourseDeleteView.as_view(), name='courses-delete'),
    path('user_register/', UserRegisterView.as_view(), name='user-register'),
    path('user_overview/', UserOverviewView.as_view(), name='user-overview'),
    path('user_history/', UserHistoryView.as_view(), name='user-history'),
    path('user_login/', LoginView.as_view(), name = 'user-login'),
    path('user_logout/', LogoutView.as_view(), name = 'user-logout')
]