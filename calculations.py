from models import Financial


def calculate_z_score(financial: Financial) -> float:
    x1 = financial.working_capital / financial.total_assets
    x2 = financial.retained_earnings / financial.total_assets
    x3 = financial.ebit / financial.total_assets
    x4 = financial.equity / financial.total_liabilities
    x5 = financial.sales / financial.total_assets
    return 1.2 * x1 + 1.4 * x2 + 3.3 * x3 + 0.6 * x4 + 1.0 * x5