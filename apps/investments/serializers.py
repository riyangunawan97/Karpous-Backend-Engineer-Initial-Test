from rest_framework import serializers
from .models import Investment, TransactionLog
import uuid

class InvestmentSerializer(serializers.ModelSerializer):
    profit_loss = serializers.SerializerMethodField()
    profit_loss_percentage = serializers.SerializerMethodField()

    class Meta:
        model = Investment
        fields = [
            'id', 'asset_name', 'amount_invested', 'current_value',
            'profit_loss', 'profit_loss_percentage', 'purchase_date'
        ]

    def get_profit_loss(self, obj):
        return f"{obj.profit_loss:.2f}"

    def get_profit_loss_percentage(self, obj):
        return f"{obj.profit_loss_percentage:.2f}"

class InvestmentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Investment
        fields = ['asset_name', 'amount_invested', 'current_value', 'purchase_date']

    def validate_amount_invested(self, value):
        if value < 1000:
            raise serializers.ValidationError("Minimum investment is $1000")
        return value

    def create(self, validated_data):
        user = self.context['request'].user
        investment = Investment.objects.create(user=user, **validated_data)

        TransactionLog.objects.create(
            user=user,
            transaction_type='PURCHASE',
            amount=validated_data['amount_invested'],
            reference_id=str(uuid.uuid4())
        )
        return investment
