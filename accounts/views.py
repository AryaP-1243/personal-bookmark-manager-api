from django.shortcuts import redirect
from django.conf import settings
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView

from .serializers import UserSerializer


class GoogleLogin(SocialLoginView):
    """
    Google OAuth2 login view.
    
    POST /api/auth/google/
    
    Request body:
    {
        "code": "authorization_code_from_google"
    }
    
    OR
    
    {
        "access_token": "google_access_token"
    }
    
    Returns auth token on success.
    """
    adapter_class = GoogleOAuth2Adapter
    callback_url = None  # Will be set dynamically
    client_class = OAuth2Client
    
    def get_callback_url(self):
        """Get the callback URL for OAuth."""
        return self.request.build_absolute_uri('/api/auth/google/callback/')


@api_view(['GET'])
@permission_classes([AllowAny])
def google_login_redirect(request):
    """
    Redirect to Google OAuth login page.
    
    This endpoint initiates the OAuth flow by redirecting to Google's login page.
    After successful login, Google will redirect back to the callback URL.
    """
    from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
    from urllib.parse import urlencode
    
    # Build the Google OAuth URL
    google_auth_url = 'https://accounts.google.com/o/oauth2/v2/auth'
    
    client_id = settings.SOCIALACCOUNT_PROVIDERS.get('google', {}).get('APP', {}).get('client_id', '')
    
    # If client_id is not in settings, try to get from SocialApp model
    if not client_id:
        try:
            from allauth.socialaccount.models import SocialApp
            app = SocialApp.objects.get(provider='google')
            client_id = app.client_id
        except:
            return JsonResponse({
                'error': 'Google OAuth not configured',
                'message': 'Please configure Google OAuth credentials in admin'
            }, status=500)
    
    callback_url = request.build_absolute_uri('/api/auth/google/callback/')
    
    params = {
        'client_id': client_id,
        'redirect_uri': callback_url,
        'scope': 'email profile',
        'response_type': 'code',
        'access_type': 'online',
    }
    
    auth_url = f"{google_auth_url}?{urlencode(params)}"
    
    return JsonResponse({
        'auth_url': auth_url,
        'message': 'Redirect to this URL to initiate Google OAuth login'
    })


@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def google_callback(request):
    """
    Handle Google OAuth callback.
    
    GET: Handles redirect from Google with authorization code
    POST: Accepts authorization code and exchanges it for access token
    
    Returns authentication token on success.
    """
    code = request.GET.get('code') or request.data.get('code')
    
    if not code:
        return Response({
            'error': 'Missing authorization code',
            'message': 'No code parameter received from Google'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # For GET requests (browser redirects), show a simple response
    # The actual token exchange should happen via the GoogleLogin view
    if request.method == 'GET':
        return JsonResponse({
            'message': 'Authorization code received',
            'code': code,
            'next_step': 'POST this code to /api/auth/google/ to get your auth token'
        })
    
    # For POST requests, return info about using the GoogleLogin endpoint
    return Response({
        'message': 'Use POST /api/auth/google/ with the code to complete login',
        'code': code
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    """
    Get the current authenticated user's profile.
    
    GET /api/auth/user/
    
    Requires authentication token in header:
    Authorization: Token <your_token>
    """
    serializer = UserSerializer(request.user)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    """
    Logout the current user by deleting their auth token.
    
    POST /api/auth/logout/
    
    Requires authentication token in header:
    Authorization: Token <your_token>
    """
    try:
        request.user.auth_token.delete()
        return Response({
            'message': 'Successfully logged out'
        }, status=status.HTTP_200_OK)
    except:
        return Response({
            'message': 'Logged out'
        }, status=status.HTTP_200_OK)
