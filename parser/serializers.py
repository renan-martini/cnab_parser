from rest_framework import serializers
from .models import Transaction, Type


class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = "__all__"


class TransactionSerializer(serializers.ModelSerializer):
    type = TypeSerializer(read_only=True)

    class Meta:
        model = Transaction
        fields = "__all__"

    def create(self, validated_data):
        transaction, _ = Transaction.objects.get_or_create(**validated_data)
        return transaction


class UploadSerializer(serializers.Serializer):
    file = serializers.FileField()

    class Meta:
        fields = ["file"]


class StoreSerializer(serializers.ModelSerializer):
    value = serializers.FloatField()
    store = serializers.CharField()
    owner = serializers.CharField()
    operations = TransactionSerializer(many=True)

    class Meta:
        fields = "__all__"
