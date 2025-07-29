from django.urls import path

from .views import (
    CreateOrderView,
    MenuItemList,
    OrderListView,
    OrderRetrieveView,
    
    RegisterView,
     MyTokenObtainPairView,
    # login_view,
    # logout_view,
    # session_view,
    # whoami_view,
    # get_csrf,  
    # session_view,
    # get_enriched_menu,
    # test_gemini,
    TableList, 
    CreateBooking,
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path("menu-items/", MenuItemList.as_view(), name='menu-item-list'),
    path('orders/', OrderListView.as_view(), name='order-list'),

    path('orders/create/', CreateOrderView.as_view(), name='create-order'),
    path('orders/<int:pk>/', OrderRetrieveView.as_view(), name='order-detail'),

    # JWT auth
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Session auth (if using)
    # path('csrf/', get_csrf, name='api-csrf'),
    # path('login/', login_view, name='api-login'),
    # path('logout/', logout_view, name='api-logout'),
    # path('session/', session_view, name='api-session'),
    # path('whoami/', whoami_view, name='api-whoami'),
    
    # path('api/session/', session_view, name='session'),
    
    # path("menu/", get_enriched_menu, name="get_enriched_menu"),
    # path("test-gemini/", test_gemini, name='test-gemini'),

    path('tables/', TableList.as_view(), name='table-list'),
    path('bookings/create/', CreateBooking.as_view(), name='create-booking'),
    
    
]
