from rest_framework import viewsets

from jailbreak import serializers, models

class CustomChatColorViewSet(viewsets.ModelViewSet):
    queryset = models.CustomChatColor.objects.all()
    serializer_class = serializers.CustomChatColorSerializer

class StorePlayerViewSet(viewsets.ModelViewSet):
    queryset = models.StorePlayer.objects.all()
    serializer_class = serializers.StorePlayerSerializer

class StoreItemViewSet(viewsets.ModelViewSet):
    queryset = models.StoreItem.objects.all()
    serializer_class = serializers.StoreItemSerializer

class StoreEquipmentViewSet(viewsets.ModelViewSet):
    queryset = models.StoreEquipment.objects.all()
    serializer_class = serializers.StoreEquipmentSerializer

class SourceModAdminViewSet(viewsets.ModelViewSet):
    queryset = models.SourceModAdmin.objects.all()
    serializer_class = serializers.SourceModAdminSerializer

class SourceModGroupViewSet(viewsets.ModelViewSet):
    queryset = models.SourceModGroup.objects.all()
    serializer_class = serializers.SourceModGroupSerializer
