import pandas as pd
from datetime import datetime, timedelta


def generate_excel(filename, profile_type):
    columns = [
        'reporting_date', 'net_profit', 'ebit', 'sales_revenue',
        'depreciation', 'operating_expenses', 'total_assets',
        'current_assets', 'inventory', 'cash', 'total_liabilities',
        'short_term_liabilities', 'equity', 'retained_earnings'
    ]

    data = []
    base_date = datetime(2024, 1, 1)

    for i in range(12):
        d = (base_date + timedelta(days=i * 30)).replace(day=1)

        if profile_type == "SANATOASA":
            # Profit solid, lichiditate mare, capital propriu puternic
            row = {
                'reporting_date': d.strftime('%Y-%m-%d'),
                'net_profit': 90000, 'ebit': 110000, 'sales_revenue': 700000,
                'depreciation': 10000, 'operating_expenses': 500000,
                'total_assets': 1500000, 'current_assets': 800000, 'inventory': 100000,
                'cash': 300000, 'total_liabilities': 300000, 'short_term_liabilities': 150000,
                'equity': 1200000, 'retained_earnings': 500000
            }
        elif profile_type == "MEDIE":
            # Profit la limita, datorii egale cu activele circulante
            row = {
                'reporting_date': d.strftime('%Y-%m-%d'),
                'net_profit': 5000, 'ebit': 8000, 'sales_revenue': 300000,
                'depreciation': 3000, 'operating_expenses': 285000,
                'total_assets': 600000, 'current_assets': 250000, 'inventory': 150000,
                'cash': 15000, 'total_liabilities': 400000, 'short_term_liabilities': 250000,
                'equity': 200000, 'retained_earnings': 40000
            }
        else:  # FALIMENT
            # Pierderi masive, capital negativ, datorii sufocante
            row = {
                'reporting_date': d.strftime('%Y-%m-%d'),
                'net_profit': -70000, 'ebit': -60000, 'sales_revenue': 120000,
                'depreciation': 2000, 'operating_expenses': 180000,
                'total_assets': 350000, 'current_assets': 60000, 'inventory': 40000,
                'cash': 1000, 'total_liabilities': 500000, 'short_term_liabilities': 450000,
                'equity': -150000, 'retained_earnings': -250000
            }
        data.append(row)

    df = pd.DataFrame(data)
    df.to_excel(filename, index=False)
    print(f"Generat: {filename}")


# Generăm cele 3 fișiere
generate_excel("firma_sanatoasa.xlsx", "SANATOASA")
generate_excel("firma_risc_mediu.xlsx", "MEDIE")
generate_excel("firma_falimentara.xlsx", "FALIMENT")