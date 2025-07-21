from django.urls import include, path
from .views import MenuItemList, OrderListCreateView, OrderDetailView, get_notes
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views

urlpatterns = [
    path("menu-item/", MenuItemList.as_view(), name='menu-item-list'),
    path('menu-orders/', OrderListCreateView.as_view(),name='order-list-create'), 
    path('menu-orders/<int:pk>/', OrderDetailView.as_view(),name='order-detail'),
    path('notes/', get_notes),
    
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    path("login", views.login, name='login'),
    path("logout", views.logout, name='logout'),
    path("register/", views.register, name="register"),
]
