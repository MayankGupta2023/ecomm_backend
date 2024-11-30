from django.urls import path
from api.views import user_views as views

urlpatterns = [
    path('register/', views.registerUser, name='register'),
    path('login/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('profile/', views.getUserProfile, name='users_profile'),
    path('profile/update/', views.updateUserProfile, name='user_profile_update'),
    # path('update/<str:pk>/', views.updateUser, name='user_update'),
    path('delete/<str:pk>/', views.deleteUser, name='user_delete'), 
]
