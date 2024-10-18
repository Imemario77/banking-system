from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

def get_access_token_from_refresh(token):
    try:
        # Decode the refresh token to get the user associated with it
        refresh = RefreshToken(token)
        # Generate a new access token from the refresh token
        return str(refresh.access_token)
    except TokenError:
        # Handle invalid token errors (e.g., token expired or malformed)
        return None
