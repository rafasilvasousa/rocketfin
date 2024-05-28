from django.contrib import admin
from django.urls import path , include
from rest_framework import routers
from rocketapi.views import LoginViewSet, AccountViewSet, PaymentViewSet, RegisterViewSet, CheckUsernameViewSet, PayeeViewSet

router = routers.DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    #path('admin/', admin.site.urls),
    path('login/', LoginViewSet.as_view({'post': 'post'}), name='login'),
    path('register/', RegisterViewSet.as_view({'post': 'post'}), name='register'),
    path('check-username/', CheckUsernameViewSet.as_view({'post': 'post'}), name='check-username'),
    path('payees/', PayeeViewSet.as_view({'get': 'list', 'post': 'create'}), name='payees'),
    path('accounts/', AccountViewSet.as_view({'get': 'list', 'post': 'create'}), name='accounts'),
    path('payments/', PaymentViewSet.as_view({'get': 'list', 'post': 'create', 'patch': 'partial_update'}), name='payments'),
    
]
