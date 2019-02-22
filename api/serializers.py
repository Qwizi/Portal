from rest_framework import serializers
from user_centrum.models import ApplicationComments

class ApplicationsCommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationComments
        fields = '__all__'