# In destinations/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'destinations'

router = DefaultRouter()
router.register(r'destinations', views.DestinationViewSet, basename='destination')

urlpatterns = [
    path('api/', include(router.urls)),  # This will include all DRF ViewSet URLs
    
    # Template views
    path('', views.DestinationListView.as_view(), name='destination-list'),
    path('add/', views.DestinationCreateView.as_view(), name='destination-create'),
    path('<slug:slug>/', views.DestinationDetailView.as_view(), name='destination-detail'),
    path('<slug:slug>/update/', views.DestinationUpdateView.as_view(), name='destination-update'),
    path('<slug:slug>/delete/', views.destination_delete, name='destination-delete'),
    path('image/<int:pk>/delete/', views.delete_destination_image, name='delete-destination-image'),
]