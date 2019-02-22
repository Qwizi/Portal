from rest_framework.authentication import TokenAuthentication
from accounts.models.token import MyToken

class MyTokenAuthentication(TokenAuthentication):
    model = MyToken