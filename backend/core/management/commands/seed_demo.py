import calendar
from datetime import date
from io import BytesIO

import pandas as pd

from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.utils import timezone

from core.models import (
    BaseReport,
    Company,
    CustomReport,
    FinancialUpload,
    MLModelVersion,
    ReportRequest,
)
from core.services import (
    auto_assign_analyst,
    generate_custom_report_pdf,
    process_financial_upload,
)


User = get_user_model()

DEMO_PASSWORD = "Demo123!"


def month_end(year: int, month: int) -> date:
    last_day = calendar.monthrange(year, month)[1]
    return date(year, month, last_day)


def previous_months(end_year=2026, end_month=5, periods=12):
    months = []

    year = end_year
    month = end_month

    for _ in range(periods):
        months.append(month_end(year, month))

        month -= 1
        if month == 0:
            month = 12
            year -= 1

    return list(reversed(months))


def generate_financial_dataframe(profile: str, periods: int = 12) -> pd.DataFrame:
    dates = previous_months(periods=periods)

    profiles = {
        "stable": {
            "base_assets": 1_500_000,
            "base_revenue": 500_000,
            "asset_growth": 0.015,
            "revenue_growth": 0.020,
            "net_margin": 0.18,
            "gross_margin": 0.38,
            "liability_ratio": 0.28,
            "current_asset_ratio": 0.55,
            "cash_ratio": 0.14,
            "inventory_ratio": 0.16,
            "short_liability_ratio": 0.38,
        },
        "medium": {
            "base_assets": 1_250_000,
            "base_revenue": 390_000,
            "asset_growth": 0.006,
            "revenue_growth": 0.004,
            "net_margin": 0.055,
            "gross_margin": 0.24,
            "liability_ratio": 0.58,
            "current_asset_ratio": 0.42,
            "cash_ratio": 0.055,
            "inventory_ratio": 0.22,
            "short_liability_ratio": 0.58,
        },
        "risk": {
            "base_assets": 950_000,
            "base_revenue": 310_000,
            "asset_growth": -0.003,
            "revenue_growth": -0.010,
            "net_margin": -0.035,
            "gross_margin": 0.13,
            "liability_ratio": 0.84,
            "current_asset_ratio": 0.31,
            "cash_ratio": 0.025,
            "inventory_ratio": 0.23,
            "short_liability_ratio": 0.72,
        },
    }

    config = profiles[profile]
    rows = []
    previous_sales = config["base_revenue"] * 0.98

    for index, reporting_date in enumerate(dates):
        total_assets = config["base_assets"] * (1 + config["asset_growth"]) ** index
        sales_revenue = config["base_revenue"] * (1 + config["revenue_growth"]) ** index

        net_profit = sales_revenue * config["net_margin"]
        gross_profit = sales_revenue * config["gross_margin"]
        depreciation = total_assets * 0.012
        ebit = net_profit + depreciation + sales_revenue * 0.025

        total_liabilities = total_assets * config["liability_ratio"]
        short_term_liabilities = total_liabilities * config["short_liability_ratio"]
        equity = total_assets - total_liabilities

        current_assets = total_assets * config["current_asset_ratio"]
        inventory = current_assets * config["inventory_ratio"]
        cash = total_assets * config["cash_ratio"]

        retained_earnings = max(equity * 0.18, 1_000)
        short_term_securities = cash * 0.18
        receivables = sales_revenue * 0.16

        operating_expenses = max(sales_revenue - gross_profit + depreciation, 1)
        financial_expenses = max(total_liabilities * 0.018, 1)
        interest = financial_expenses * 0.45

        share_capital = max(equity * 0.32, 1_000)
        profit_on_operating_activities = ebit - financial_expenses
        gross_profit_3_years = gross_profit * 2.4
        cost_of_products_sold = sales_revenue - gross_profit
        profit_on_sales = gross_profit - operating_expenses * 0.18
        total_costs = sales_revenue - net_profit

        rows.append(
            {
                "reporting_date": reporting_date,
                "net_profit": round(net_profit, 2),
                "ebit": round(ebit, 2),
                "sales_revenue": round(sales_revenue, 2),
                "depreciation": round(depreciation, 2),
                "operating_expenses": round(operating_expenses, 2),
                "total_assets": round(total_assets, 2),
                "current_assets": round(current_assets, 2),
                "inventory": round(inventory, 2),
                "cash": round(cash, 2),
                "total_liabilities": round(total_liabilities, 2),
                "short_term_liabilities": round(short_term_liabilities, 2),
                "equity": round(equity, 2),
                "retained_earnings": round(retained_earnings, 2),
                "short_term_securities": round(short_term_securities, 2),
                "receivables": round(receivables, 2),
                "gross_profit": round(gross_profit, 2),
                "extraordinary_items": 0,
                "financial_expenses": round(financial_expenses, 2),
                "interest": round(interest, 2),
                "share_capital": round(share_capital, 2),
                "profit_on_operating_activities": round(profit_on_operating_activities, 2),
                "gross_profit_3_years": round(gross_profit_3_years, 2),
                "cost_of_products_sold": round(cost_of_products_sold, 2),
                "profit_on_sales": round(profit_on_sales, 2),
                "total_costs": round(total_costs, 2),
                "previous_period_sales": round(previous_sales, 2),
            }
        )

        previous_sales = sales_revenue

    return pd.DataFrame(rows)


def dataframe_to_excel_content(df: pd.DataFrame) -> ContentFile:
    buffer = BytesIO()

    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="financial_data")

    return ContentFile(buffer.getvalue())


class Command(BaseCommand):
    help = "Populează baza de date cu utilizatori, companii, importuri și rapoarte pentru demo."

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING("Pornesc popularea demo..."))

        analysts = self.create_analysts()
        clients = self.create_clients_and_companies(analysts)
        self.create_report_scenarios(clients)

        self.stdout.write(self.style.SUCCESS("Populare demo finalizată."))
        self.stdout.write("")
        self.stdout.write("Conturi demo:")
        self.stdout.write(f"Parolă comună: {DEMO_PASSWORD}")
        self.stdout.write("Analist exemplu: analyst1")
        self.stdout.write("Client stabil exemplu: client_stabil_1")
        self.stdout.write("Client risc exemplu: client_risc_1")
        self.stdout.write("Client nou fără onboarding: client_nou")

    def create_user(self, username, email, role, is_staff=False):
        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                "email": email,
                "role": role,
                "is_staff": is_staff,
            },
        )

        user.email = email
        user.role = role
        user.is_staff = is_staff
        user.set_password(DEMO_PASSWORD)
        user.save()

        return user, created

    def create_analysts(self):
        analysts = []

        for index in range(1, 6):
            analyst, created = self.create_user(
                username=f"analyst{index}",
                email=f"analyst{index}@demo.ro",
                role="analyst",
                is_staff=False,
            )

            analysts.append(analyst)

            if created:
                self.stdout.write(f"Analist creat: {analyst.username}")
            else:
                self.stdout.write(f"Analist existent actualizat: {analyst.username}")

        return analysts

    def create_clients_and_companies(self, analysts):
        scenarios = [
            {
                "username": "client_nou",
                "email": "client_nou@demo.ro",
                "company": None,
            },
            {
                "username": "client_fara_import",
                "email": "client_fara_import@demo.ro",
                "company": {
                    "name": "SC Start Demo SRL",
                    "cui": "RO90000001",
                    "industry": "Servicii",
                    "profile": "stable",
                    "status": "no_upload",
                    "periods": 12,
                },
            },
            {
                "username": "client_pending",
                "email": "client_pending@demo.ro",
                "company": {
                    "name": "SC Pending Finance SRL",
                    "cui": "RO90000002",
                    "industry": "Comerț",
                    "profile": "medium",
                    "status": "pending",
                    "periods": 12,
                },
            },
            {
                "username": "client_respins",
                "email": "client_respins@demo.ro",
                "company": {
                    "name": "SC Import Respins SRL",
                    "cui": "RO90000003",
                    "industry": "Retail",
                    "profile": "risk",
                    "status": "rejected",
                    "periods": 12,
                },
            },
            {
                "username": "client_stabil_1",
                "email": "client_stabil_1@demo.ro",
                "company": {
                    "name": "SC Alpha Stabil SRL",
                    "cui": "RO90000004",
                    "industry": "IT",
                    "profile": "stable",
                    "status": "approved",
                    "periods": 24,
                },
            },
            {
                "username": "client_stabil_2",
                "email": "client_stabil_2@demo.ro",
                "company": {
                    "name": "SC Beta Consult SRL",
                    "cui": "RO90000005",
                    "industry": "Consultanță",
                    "profile": "stable",
                    "status": "approved",
                    "periods": 12,
                },
            },
            {
                "username": "client_stabil_3",
                "email": "client_stabil_3@demo.ro",
                "company": {
                    "name": "SC Gamma Services SRL",
                    "cui": "RO90000006",
                    "industry": "Servicii",
                    "profile": "stable",
                    "status": "approved",
                    "periods": 18,
                },
            },
            {
                "username": "client_stabil_4",
                "email": "client_stabil_4@demo.ro",
                "company": {
                    "name": "SC Delta Market SRL",
                    "cui": "RO90000007",
                    "industry": "Distribuție",
                    "profile": "stable",
                    "status": "approved",
                    "periods": 12,
                },
            },
            {
                "username": "client_mediu_1",
                "email": "client_mediu_1@demo.ro",
                "company": {
                    "name": "SC Mediu Construct SRL",
                    "cui": "RO90000008",
                    "industry": "Construcții",
                    "profile": "medium",
                    "status": "approved",
                    "periods": 12,
                },
            },
            {
                "username": "client_mediu_2",
                "email": "client_mediu_2@demo.ro",
                "company": {
                    "name": "SC Mediu Retail SRL",
                    "cui": "RO90000009",
                    "industry": "Retail",
                    "profile": "medium",
                    "status": "approved",
                    "periods": 12,
                },
            },
            {
                "username": "client_risc_1",
                "email": "client_risc_1@demo.ro",
                "company": {
                    "name": "SC Risc Industrial SRL",
                    "cui": "RO90000010",
                    "industry": "Producție",
                    "profile": "risk",
                    "status": "approved",
                    "periods": 12,
                },
            },
            {
                "username": "client_raport",
                "email": "client_raport@demo.ro",
                "company": {
                    "name": "SC Raport Expert SRL",
                    "cui": "RO90000011",
                    "industry": "Servicii financiare",
                    "profile": "medium",
                    "status": "approved",
                    "periods": 12,
                    "create_reports": True,
                },
            },
        ]

        created_clients = []

        for scenario in scenarios:
            client, _ = self.create_user(
                username=scenario["username"],
                email=scenario["email"],
                role="client",
                is_staff=False,
            )

            company_config = scenario.get("company")

            if not company_config:
                created_clients.append(client)
                self.stdout.write(f"Client fără companie: {client.username}")
                continue

            company, _ = Company.objects.get_or_create(
                cui=company_config["cui"],
                defaults={
                    "name": company_config["name"],
                    "industry": company_config["industry"],
                    "address": "București, România",
                    "phone_number": "0722000000",
                    "email_contact": scenario["email"],
                    "owner": client,
                    "is_onboarded": False,
                },
            )

            company.name = company_config["name"]
            company.industry = company_config["industry"]
            company.owner = client
            company.address = "București, România"
            company.phone_number = "0722000000"
            company.email_contact = scenario["email"]

            if not company.analyst:
                auto_assign_analyst(company)

            company.save()

            self.prepare_company_import(company, company_config)

            created_clients.append(client)

        return created_clients

    def prepare_company_import(self, company, company_config):
        status_value = company_config["status"]

        if status_value == "no_upload":
            self.stdout.write(f"Companie fără import: {company.name}")
            return

        if company.uploads.exists():
            self.stdout.write(f"Compania are deja importuri, sar peste: {company.name}")
            return

        df = generate_financial_dataframe(
            profile=company_config["profile"],
            periods=company_config["periods"],
        )

        excel_content = dataframe_to_excel_content(df)
        file_name = f"{company.cui}_demo_import.xlsx"

        upload = FinancialUpload(
            company=company,
            status="pending",
        )
        upload.file.save(file_name, excel_content, save=True)

        if status_value == "pending":
            self.stdout.write(f"Import pending creat pentru: {company.name}")
            return

        if status_value == "rejected":
            upload.status = "rejected"
            upload.processed_by = company.analyst
            upload.processed_at = timezone.now()
            upload.rejection_reason = (
                "Fișier respins pentru demo: valorile financiare necesită corectare "
                "înainte de procesare."
            )
            upload.save()

            self.stdout.write(f"Import respins creat pentru: {company.name}")
            return

        if status_value == "approved":
            success, message = process_financial_upload(upload)

            if success:
                upload.refresh_from_db()
                upload.processed_by = company.analyst
                upload.save()

                self.stdout.write(
                    self.style.SUCCESS(f"Import aprobat și procesat pentru: {company.name}")
                )
            else:
                self.stdout.write(
                    self.style.ERROR(
                        f"Procesarea a eșuat pentru {company.name}: {message}"
                    )
                )

    def create_report_scenarios(self, clients):
        company = Company.objects.filter(cui="RO90000011").first()

        if not company:
            return

        base_report = BaseReport.objects.filter(
            snapshot__statement__company=company
        ).select_related(
            "snapshot",
            "snapshot__statement",
        ).order_by("-snapshot__statement__reporting_date").first()

        if not base_report:
            return

        pending_request, _ = ReportRequest.objects.get_or_create(
            company=company,
            base_report=base_report,
            analyst=company.analyst,
            client_message=(
                "Aș dori o analiză suplimentară privind evoluția lichidității "
                "și a gradului de îndatorare."
            ),
            status="pending",
        )

        completed_request, _ = ReportRequest.objects.get_or_create(
            company=company,
            base_report=base_report,
            analyst=company.analyst,
            client_message=(
                "Solicit o interpretare personalizată a riscului financiar și "
                "recomandări pentru următoarele luni."
            ),
            status="completed",
        )

        custom_report, _ = CustomReport.objects.get_or_create(
            request=completed_request,
            defaults={
                "analyst_message": (
                    "Compania prezintă o situație financiară relativ stabilă, "
                    "însă este recomandată monitorizarea atentă a lichidității."
                ),
                "expert_recommendations": (
                    "Se recomandă reducerea expunerii pe datorii curente, "
                    "creșterea nivelului de numerar disponibil și urmărirea lunară "
                    "a marjei de profit."
                ),
                "extra_data_json": {
                    "lichiditate": "Monitorizare lunară a lichidității curente.",
                    "profitabilitate": "Menținerea controlului asupra costurilor operaționale.",
                    "indatorare": "Reducerea graduală a obligațiilor pe termen scurt.",
                },
            },
        )

        generate_custom_report_pdf(custom_report)

        self.stdout.write("Solicitări de rapoarte demo create.")