from django.urls import path

from .views import (IpoListView,
                    IpoBidCreateView,
                    IpoBidDeleteView,
                    IpoBidUpdateView,
                    IpoCloseView
                    
)

app_name = 'ipo'
urlpatterns = [
    path('ipo_list/', IpoListView.as_view(), name='ipo-list'),
    path('<int:id>/ipo_bid/', IpoBidCreateView.as_view(), name='ipo-bid'),
    path('<int:id>/ipo_delete/', IpoBidDeleteView.as_view(), name='ipo-delete'),
    path('<int:id>/ipo_update/', IpoBidUpdateView.as_view(), name='ipo-update'),
    path('<int:id>/ipo_close/', IpoCloseView.as_view(), name='ipo-close')
    
]