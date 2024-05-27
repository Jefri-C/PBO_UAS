from rest_framework import serializers
from pbo_uas.models import ProductCategory

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ['id', 'name']
