from rest_framework.response import Response

from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_POST
from django.middleware.csrf import get_token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.views.decorators.csrf import csrf_protect
import json,requests
from .utils.gemini import enrich_menu_item
from .models import MenuItem, Order
from .serializers import MenuItemSerializer, OrderSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication

UNSPLASH_ACCESS_KEY = 'bRSY6Ar9PUb1986rvzrDGYSX2ZUpbq7JF1x_mapdeTk'

def fetch_unsplash_image(query):
    url = "https://api.unsplash.com/search/photos"
    headers = {"Accept-Version": "v1"}
    params = {
        "query": query,
        "client_id": UNSPLASH_ACCESS_KEY,
        "per_page": 1,
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        if data["results"]:
            return data["results"][0]["urls"]["small"]
    return None

class MenuItemList(generics.ListCreateAPIView):
    serializer_class = MenuItemSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return MenuItem.objects.filter(is_available=True)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data

        # Attach image_url from Unsplash for each item
        for item in data:
            image_url = fetch_unsplash_image(item['name'])
            item['image_url'] = image_url or ''

        return Response(data)

class OrderListCreateView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    
def get_csrf(request):
    response = JsonResponse({'detail': 'CSRF cookie set'})
    response['X-CSRFToken'] = get_token(request)
    return response

@api_view(["GET"])
@permission_classes([AllowAny])
@ensure_csrf_cookie
def session_view(request):
    return JsonResponse({
        "isAuthenticated": request.user.is_authenticated
    })


@api_view(["POST"])
@permission_classes([AllowAny])  # <-- add this!
@csrf_protect
def login_view(request):
    data = request.data
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return JsonResponse({'detail': 'Missing credentials'}, status=400)

    user = authenticate(request, username=username, password=password)
    if user is None:
        return JsonResponse({'detail': 'Invalid credentials'}, status=401)

    login(request, user)
    return JsonResponse({'detail': 'Successfully logged in'})


@api_view(["POST"])
def logout_view(request):
    if not request.user.is_authenticated:
        return JsonResponse({'detail': "You're not logged in."}, status=400)

    logout(request)
    return JsonResponse({'detail': 'Successfully logged out'})


@api_view(["GET"])
def whoami_view(request):
    if not request.user.is_authenticated:
        return JsonResponse({'isAuthenticated': False})

    return JsonResponse({'username': request.user.username})






BASE_MENU = {
    "foods": [
        {"title": "Veg Burger", "price": "$5", "tags": "Spicy, Grilled"},
        {"title": "Paneer Wrap", "price": "$6", "tags": "Indian, Grilled"},
    ],
    "drinks": [
        {"title": "Lemonade", "price": "$2", "tags": "Cold, Fresh"},
        {"title": "Iced Tea", "price": "$2.5", "tags": "Chilled, Caffeinated"},
    ]
}

def get_enriched_menu(request):
    enriched_menu = {"foods": [], "drinks": []}

    for item in BASE_MENU["foods"]:
        gemini_data = enrich_menu_item(item["title"])
        enriched_menu["foods"].append({**item, **gemini_data})

    for item in BASE_MENU["drinks"]:
        gemini_data = enrich_menu_item(item["title"])
        enriched_menu["drinks"].append({**item, **gemini_data})

    return JsonResponse(enriched_menu)

def test_gemini(request):
    result = enrich_menu_item("Cheese Sandwich")
    return JsonResponse(result)