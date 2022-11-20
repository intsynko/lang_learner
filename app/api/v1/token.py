from rest_framework_simplejwt.views import TokenObtainPairView as TokenObtainPairView_


class TokenObtainPairView(TokenObtainPairView_):
    """
    Takes a set of user credentials and returns an access and refresh JSON web
    token pair to prove the authentication of those credentials.
    """

    _serializer_class = settings.TOKEN_OBTAIN_SERIALIZER
