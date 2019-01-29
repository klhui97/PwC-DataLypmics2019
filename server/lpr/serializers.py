from rest_framework import serializers
from lpr.models import LrpModel

class ConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = LrpModel
        fields = "__all__"