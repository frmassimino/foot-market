from django.urls import path

from .views import (PlayersList,
)

app_name = 'player'
urlpatterns = [
    #path('', CourseView.as_view(template_name='contact.html'), name='courses-list'),
    #path('', my_fbv, name='courses-list'),
    #path('<int:id>/', CourseView.as_view(), name='courses-detail'),
    #path('', CourseListView.as_view(), name='courses-list'),
    #path('', MyListView.as_view(), name='courses-list'),
    #path('create/', CourseCreateView.as_view(), name='courses-create'),
    #path('<int:id>/update/', CourseUpdateView.as_view(), name='courses-update'),
    #path('<int:id>/delete/', CourseDeleteView.as_view(), name='courses-delete'),
    path('players_list/', PlayersList.as_view(), name = 'players-list'),
    #path('bid_list/', BidListView.as_view(), name='bid-list'),
    #path('bid_create/', BidCreateView.as_view(), name='bid-create'),
    #path('bid/<int:id>/delete/', BidDeleteView.as_view(), name='bid-delete'),
    #path('ask_list/', AskListView.as_view(), name='ask-list'),
    #path('ask_create/', AskCreateView.as_view(), name='ask-create'),
    #path('ask/<int:id>/delete/', AskDeleteView.as_view(), name='ask-delete'),
]