
from rest_framework import viewsets
from user_centrum.models import ApplicationComments
from . import serializers

class ApplicationComment(viewsets.ModelViewSet):
    queryset = ApplicationComments.objects.all()
    serializer_class = serializers.ApplicationsCommentsSerializer