from .models import UserInvestment
from django.db.models import Avg

class InvestmentService:

    def calculate_portfolio_performance(self, user):
        investments = UserInvestment.objects.filter(user=user)
        total_invested = sum(i.amount_invested for i in investments)
        current_value = sum(i.current_value for i in investments)
        total_profit_loss = current_value - total_invested

        best = max(investments, key=lambda i: i.profit_loss_percentage(), default=None)
        worst = min(investments, key=lambda i: i.profit_loss_percentage(), default=None)

        return {
            "total_invested": "%.2f" % total_invested,
            "current_portfolio_value": "%.2f" % current_value,
            "total_profit_loss": "%.2f" % total_profit_loss,
            "active_investments": investments.filter(is_active=True).count(),
            "best_performing": best.asset_name if best else None,
            "worst_performing": worst.asset_name if worst else None,
        }

    def get_investment_insights(self, user):
        investments = UserInvestment.objects.filter(user=user)
        avg_investment = investments.aggregate(Avg('amount_invested'))['amount_invested__avg']
        return {
            "average_investment_size": "%.2f" % (avg_investment or 0),
        }
