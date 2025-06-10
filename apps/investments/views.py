from rest_framework import generics, permissions, response
from .models import Investment
from .serializers import InvestmentSerializer, InvestmentCreateSerializer
from .services import InvestmentService
from django.db.models import Sum, F

class ListUserInvestmentsView(generics.ListAPIView):
    serializer_class = InvestmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Investment.objects.filter(user=self.request.user).order_by('-purchase_date')

class CreateInvestmentView(generics.CreateAPIView):
    serializer_class = InvestmentCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

class InvestmentSummaryView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        investments = Investment.objects.filter(user=user, is_active=True)

        total_invested = investments.aggregate(Sum('amount_invested'))['amount_invested__sum'] or 0
        total_current = investments.aggregate(Sum('current_value'))['current_value__sum'] or 0
        total_profit = total_current - total_invested
        count = investments.count()

        best = max(investments, key=lambda inv: inv.profit_loss, default=None)
        worst = min(investments, key=lambda inv: inv.profit_loss, default=None)

        return response.Response({
            'total_invested': f"{total_invested:.2f}",
            'current_portfolio_value': f"{total_current:.2f}",
            'total_profit_loss': f"{total_profit:.2f}",
            'number_of_active_investments': count,
            'best_performing_investment': best.asset_name if best else None,
            'worst_performing_investment': worst.asset_name if worst else None,
        })
