from rest_framework import serializers
from .models import Fruits, Images


class FruitsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fruits
        fields = ("title", "price", "stock", "sold")

class ImagesSerializers(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = ("image")


