from rest_framework import serializers
from rest_framework.response import Response

from .models import CustomChatColor, StorePlayer, StoreItem, StoreEquipment, SourceModAdmin, SourceModGroup

from jailbreak import models

class CustomChatColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomChatColor
        fields = '__all__'

class StorePlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = StorePlayer
        fields = '__all__'

class StoreItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoreItem
        fields = '__all__'

class StoreEquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoreEquipment
        fields = '__all__'


class SourceModGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = SourceModGroup
        fields = '__all__'

class SourceModAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = SourceModAdmin
        fields = '__all__'