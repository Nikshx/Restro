from django.urls import path

from .views import (
    MenuItemList,
    OrderListCreateView,
    OrderDetailView,
    login_view,
    logout_view,
    session_view,
    whoami_view,
    get_csrf,  
    session_view,
    get_enriched_menu,
    test_gemini,
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path("menu-item/", MenuItemList.as_view(), name='menu-item-list'),
    path("menu-orders/", OrderListCreateView.as_view(), name='order-list-create'),
    path("menu-orders/<int:pk>/", OrderDetailView.as_view(), name='order-detail'),

    # JWT auth
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Session auth (if using)
    path('csrf/', get_csrf, name='api-csrf'),
    path('login/', login_view, name='api-login'),
    path('logout/', logout_view, name='api-logout'),
    path('session/', session_view, name='api-session'),
    path('whoami/', whoami_view, name='api-whoami'),
    
    # path('api/session/', session_view, name='session'),
    
    path("menu/", get_enriched_menu, name="get_enriched_menu"),
    path("test-gemini/", test_gemini, name='test-gemini'),

    
]
