from django.urls import path

from .views import (TradeStatus,
                    TradeOverview,
                    BidListView,
                    BidCreateView,
                    BidDeleteView,
                    BidUpdateView,
                    AskListView,
                    AskCreateView,
                    AskDeleteView,
                    AskUpdateView,
)

app_name = 'trade'
urlpatterns = [
    #path('', CourseView.as_view(template_name='contact.html'), name='courses-list'),
    #path('', my_fbv, name='courses-list'),
    #path('<int:id>/', CourseView.as_view(), name='courses-detail'),
    #path('', CourseListView.as_view(), name='courses-list'),
    #path('', MyListView.as_view(), name='courses-list'),
    #path('create/', CourseCreateView.as_view(), name='courses-create'),
    #path('<int:id>/update/', CourseUpdateView.as_view(), name='courses-update'),
    #path('<int:id>/delete/', CourseDeleteView.as_view(), name='courses-delete'),
    #path('<int:id>/trades_status/', TradeStatus.as_view(), name = 'trade-status'),
    path('<int:id>/trade_overview/', TradeOverview.as_view(), name = 'trade-overview'),
    path('bid_list/', BidListView.as_view(), name='bid-list'),
    path('<int:id>/bid_create/', BidCreateView.as_view(), name='bid-create'),
    path('<int:id>/bid_delete/', BidDeleteView.as_view(), name='bid-delete'),
    path('<int:id>/bid_update/', BidUpdateView.as_view(), name='bid-update'),
    path('ask_list/', AskListView.as_view(), name='ask-list'),
    path('<int:id>/ask_create/', AskCreateView.as_view(), name='ask-create'),
    path('<int:id>/ask_delete/', AskDeleteView.as_view(), name='ask-delete'),
    path('<int:id>/ask_update/', AskUpdateView.as_view(), name='ask-update'),
]