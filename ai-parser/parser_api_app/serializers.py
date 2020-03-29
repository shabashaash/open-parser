from rest_framework import serializers
from django.contrib.postgres.fields import ArrayField
from .models import Tags,Labels,Zeros,ToParse
class TagsSerializer(serializers.Serializer):
    data = serializers.ListField(child=serializers.FloatField())
    label = serializers.IntegerField()
    used = serializers.BooleanField()
    def create(self, validated_data):
        return Tags.objects.create(**validated_data)
        
class LabelsSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    number = serializers.IntegerField()
    def create(self, validated_data):
        return Labels.objects.create(**validated_data)

class ZerosSerializer(serializers.Serializer):
    true_label = serializers.IntegerField()
    data = serializers.ListField(child=serializers.FloatField())
    used = serializers.BooleanField()
    def create(self, validated_data):
        return Zeros.objects.create(**validated_data)

# class ToParseSerializer(serializers.Serializer):
#     site = serializers.CharField(max_length=255)
#     label = serializers.IntegerField()
#     tag = serializers.CharField(max_length=255)
#     ptag = serializers.CharField(max_length=255)
#     pptag = serializers.CharField(max_length=255)
#     Cclass = serializers.CharField(max_length=255)
#     pclass = serializers.CharField(max_length=255)
#     ppclass = serializers.CharField(max_length=255)
#     def create(self, validated_data):
#         return ToParse.objects.create(**validated_data)