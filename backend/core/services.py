import pandas as pd
import numpy as np
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import Count

from .ml_service import predict_risk
from .models import FinancialUpload, FinancialStatement, KPISnapshot, BaseReport


def validate_and_parse_financial_excel(file_path, is_onboarding=True):
    required_columns = [
        'reporting_date',
        'net_profit',
        'ebit',
        'sales_revenue',
        'depreciation',
        'operating_expenses',
        'total_assets',
        'current_assets',
        'inventory',
        'cash',
        'total_liabilities',
        'short_term_liabilities',
        'equity',
        'retained_earnings',
        'short_term_securities',
        'receivables',
        'gross_profit',
        'extraordinary_items',
        'financial_expenses',
        'interest',
        'share_capital',
        'profit_on_operating_activities',
        'gross_profit_3_years',
        'cost_of_products_sold',
        'profit_on_sales',
        'total_costs',
        'previous_period_sales',
    ]

    try:
        df = pd.read_excel(file_path)

        df.columns = [str(col).strip().lower() for col in df.columns]

        missing_columns = [
            col for col in required_columns
            if col not in df.columns
        ]

        if missing_columns:
            raise ValidationError(
                "Fișier incomplet. Lipsesc coloanele: "
                + ", ".join(missing_columns)
            )

        df = df.dropna(how="all").reset_index(drop=True)

        if df.empty:
            raise ValidationError(
                "Fișierul încărcat nu conține date financiare."
            )

        df['reporting_date'] = pd.to_datetime(
            df['reporting_date'],
            errors='coerce'
        )

        if df['reporting_date'].isna().any():
            raise ValidationError(
                "Coloana reporting_date conține valori lipsă sau date invalide."
            )

        reporting_months = df['reporting_date'].dt.to_period('M')

        if reporting_months.duplicated().any():
            raise ValidationError(
                "Fișierul conține mai multe înregistrări pentru aceeași lună financiară."
            )

        if is_onboarding and reporting_months.nunique() < 12:
            raise ValidationError(
                f"Onboarding eșuat. Sunt necesare minimum 12 luni financiare distincte, "
                f"dar fișierul conține doar {reporting_months.nunique()}."
            )

        if is_onboarding:
            sorted_months = sorted(reporting_months.unique())

            expected_months = pd.period_range(
                start=sorted_months[0],
                end=sorted_months[-1],
                freq='M'
            )

            if len(expected_months) != len(sorted_months):
                raise ValidationError(
                    "Pentru onboarding, perioadele financiare trebuie să reprezinte luni consecutive."
                )

        df['reporting_date'] = df['reporting_date'].dt.date

        numeric_columns = [
            col for col in required_columns
            if col != 'reporting_date'
        ]

        for col in numeric_columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

        invalid_numeric_columns = [
            col for col in numeric_columns
            if df[col].isna().any()
        ]

        if invalid_numeric_columns:
            raise ValidationError(
                "Există valori lipsă sau invalide în coloanele: "
                + ", ".join(invalid_numeric_columns)
            )

        if (df['total_assets'] <= 0).any():
            raise ValidationError(
                "Activele totale trebuie să fie mai mari decât zero."
            )

        if (df['sales_revenue'] <= 0).any():
            raise ValidationError(
                "Veniturile din vânzări trebuie să fie mai mari decât zero."
            )

        if (df['previous_period_sales'] <= 0).any():
            raise ValidationError(
                "Vânzările perioadei anterioare trebuie să fie mai mari decât zero."
            )

        non_negative_columns = {
            'current_assets': "Activele curente",
            'inventory': "Stocurile",
            'cash': "Disponibilitățile bănești",
            'total_liabilities': "Datoriile totale",
            'short_term_liabilities': "Datoriile pe termen scurt",
            'short_term_securities': "Titlurile financiare pe termen scurt",
            'receivables': "Creanțele",
            'depreciation': "Amortizarea",
            'operating_expenses': "Cheltuielile operaționale",
            'financial_expenses': "Cheltuielile financiare",
            'interest': "Dobânzile",
            'share_capital': "Capitalul social",
            'cost_of_products_sold': "Costul produselor vândute",
            'total_costs': "Costurile totale",
        }

        for column, label in non_negative_columns.items():
            if (df[column] < 0).any():
                raise ValidationError(
                    f"{label} nu pot avea valori negative."
                )

        if (df['current_assets'] > df['total_assets']).any():
            raise ValidationError(
                "Activele curente nu pot depăși activele totale."
            )

        if (df['inventory'] > df['current_assets']).any():
            raise ValidationError(
                "Stocurile nu pot depăși activele curente."
            )

        if (df['receivables'] > df['current_assets']).any():
            raise ValidationError(
                "Creanțele nu pot depăși activele curente."
            )

        if (df['cash'] > df['current_assets']).any():
            raise ValidationError(
                "Disponibilitățile bănești nu pot depăși activele curente."
            )

        if (df['short_term_securities'] > df['current_assets']).any():
            raise ValidationError(
                "Titlurile financiare pe termen scurt nu pot depăși activele curente."
            )

        if (
            df['cash']
            + df['receivables']
            + df['inventory']
            + df['short_term_securities']
            > df['current_assets']
        ).any():
            raise ValidationError(
                "Suma componentelor activelor curente "
                "(numerar, creanțe, stocuri și titluri financiare pe termen scurt) "
                "nu poate depăși valoarea activelor curente."
            )

        if (df['short_term_liabilities'] > df['total_liabilities']).any():
            raise ValidationError(
                "Datoriile pe termen scurt nu pot depăși datoriile totale."
            )

        df = df.sort_values(by='reporting_date').reset_index(drop=True)

        return df

    except ValidationError:
        raise

    except Exception as e:
        raise ValidationError(
            f"Eroare critică la citirea fișierului: {str(e)}"
        )

def calculate_kpis(df):
    """
    Calculează indicatorii financiari X1-X64 conform structurii UCI
    Polish Companies Bankruptcy Dataset, pentru fiecare perioadă financiară
    din fișierul încărcat.

    X65 și X66 sunt indicatori suplimentari creați prin feature engineering,
    identici cu cei utilizați la antrenarea modelului LightGBM.

    În aplicația curentă:
        - fiecare rând din Excel reprezintă o lună financiară;
        - fiecare lună primește propriul snapshot KPI;
        - pentru fiecare snapshot este generată propria predicție ML.
    """

    d = df.copy()

    def safe_divide(numerator, denominator):
        safe_denominator = denominator.replace(0, np.nan)
        return numerator / safe_denominator

    working_capital = (
        d['current_assets']
        - d['short_term_liabilities']
    )

    fixed_assets = (
        d['total_assets']
        - d['current_assets']
    )

    long_term_liabilities = (
        d['total_liabilities']
        - d['short_term_liabilities']
    )

    constant_capital = (
        d['equity']
        + long_term_liabilities
    )

    operating_cash_flow = (
        d['net_profit']
        + d['depreciation']
    )

    ebitda_uci = (
        d['profit_on_operating_activities']
        - d['depreciation']
    )

    d['x1'] = safe_divide(
        d['net_profit'],
        d['total_assets']
    )

    d['x2'] = safe_divide(
        d['total_liabilities'],
        d['total_assets']
    )

    d['x3'] = safe_divide(
        working_capital,
        d['total_assets']
    )

    d['x4'] = safe_divide(
        d['current_assets'],
        d['short_term_liabilities']
    )

    d['x5'] = safe_divide(
        (
            d['cash']
            + d['short_term_securities']
            + d['receivables']
            - d['short_term_liabilities']
        ),
        (
            d['operating_expenses']
            - d['depreciation']
        )
    ) * 365

    d['x6'] = safe_divide(
        d['retained_earnings'],
        d['total_assets']
    )

    d['x7'] = safe_divide(
        d['ebit'],
        d['total_assets']
    )

    d['x8'] = safe_divide(
        d['equity'],
        d['total_liabilities']
    )

    d['x9'] = safe_divide(
        d['sales_revenue'],
        d['total_assets']
    )

    d['x10'] = safe_divide(
        d['equity'],
        d['total_assets']
    )

    d['x11'] = safe_divide(
        (
            d['gross_profit']
            + d['extraordinary_items']
            + d['financial_expenses']
        ),
        d['total_assets']
    )

    d['x12'] = safe_divide(
        d['gross_profit'],
        d['short_term_liabilities']
    )

    d['x13'] = safe_divide(
        (
            d['gross_profit']
            + d['depreciation']
        ),
        d['sales_revenue']
    )

    d['x14'] = safe_divide(
        (
            d['gross_profit']
            + d['interest']
        ),
        d['total_assets']
    )

    d['x15'] = safe_divide(
        d['total_liabilities'] * 365,
        (
            d['gross_profit']
            + d['depreciation']
        )
    )

    d['x16'] = safe_divide(
        (
            d['gross_profit']
            + d['depreciation']
        ),
        d['total_liabilities']
    )

    d['x17'] = safe_divide(
        d['total_assets'],
        d['total_liabilities']
    )

    d['x18'] = safe_divide(
        d['gross_profit'],
        d['total_assets']
    )

    d['x19'] = safe_divide(
        d['gross_profit'],
        d['sales_revenue']
    )

    d['x20'] = safe_divide(
        d['inventory'] * 365,
        d['sales_revenue']
    )

    d['x21'] = safe_divide(
        d['sales_revenue'],
        d['previous_period_sales']
    )

    d['x22'] = safe_divide(
        d['profit_on_operating_activities'],
        d['total_assets']
    )

    d['x23'] = safe_divide(
        d['net_profit'],
        d['sales_revenue']
    )

    d['x24'] = safe_divide(
        d['gross_profit_3_years'],
        d['total_assets']
    )

    d['x25'] = safe_divide(
        (
            d['equity']
            - d['share_capital']
        ),
        d['total_assets']
    )

    d['x26'] = safe_divide(
        operating_cash_flow,
        d['total_liabilities']
    )

    d['x27'] = safe_divide(
        d['profit_on_operating_activities'],
        d['financial_expenses']
    )

    d['x28'] = safe_divide(
        working_capital,
        fixed_assets
    )

    d['x29'] = np.log10(
        d['total_assets'].astype(float)
    )

    d['x30'] = safe_divide(
        (
            d['total_liabilities']
            - d['cash']
        ),
        d['sales_revenue']
    )

    d['x31'] = safe_divide(
        (
            d['gross_profit']
            + d['interest']
        ),
        d['sales_revenue']
    )

    d['x32'] = safe_divide(
        d['short_term_liabilities'] * 365,
        d['cost_of_products_sold']
    )

    d['x33'] = safe_divide(
        d['operating_expenses'],
        d['short_term_liabilities']
    )

    d['x34'] = safe_divide(
        d['operating_expenses'],
        d['total_liabilities']
    )

    d['x35'] = safe_divide(
        d['profit_on_sales'],
        d['total_assets']
    )

    d['x36'] = safe_divide(
        d['sales_revenue'],
        d['total_assets']
    )

    d['x37'] = safe_divide(
        (
            d['current_assets']
            - d['inventory']
        ),
        long_term_liabilities
    )

    d['x38'] = safe_divide(
        constant_capital,
        d['total_assets']
    )

    d['x39'] = safe_divide(
        d['profit_on_sales'],
        d['sales_revenue']
    )

    d['x40'] = safe_divide(
        (
            d['current_assets']
            - d['inventory']
            - d['receivables']
        ),
        d['short_term_liabilities']
    )

    d['x41'] = safe_divide(
        d['total_liabilities'],
        (
            (
                d['profit_on_operating_activities']
                + d['depreciation']
            )
            * (12 / 365)
        )
    )

    d['x42'] = safe_divide(
        d['profit_on_operating_activities'],
        d['sales_revenue']
    )

    d['x43'] = (
        safe_divide(
            d['receivables'] * 365,
            d['sales_revenue']
        )
        + safe_divide(
            d['inventory'] * 365,
            d['cost_of_products_sold']
        )
    )

    d['x44'] = safe_divide(
        d['receivables'] * 365,
        d['sales_revenue']
    )

    d['x45'] = safe_divide(
        d['net_profit'],
        d['inventory']
    )

    d['x46'] = safe_divide(
        (
            d['current_assets']
            - d['inventory']
        ),
        d['short_term_liabilities']
    )

    d['x47'] = safe_divide(
        d['inventory'] * 365,
        d['cost_of_products_sold']
    )

    d['x48'] = safe_divide(
        ebitda_uci,
        d['total_assets']
    )

    d['x49'] = safe_divide(
        ebitda_uci,
        d['sales_revenue']
    )

    d['x50'] = safe_divide(
        d['current_assets'],
        d['total_liabilities']
    )

    d['x51'] = safe_divide(
        d['short_term_liabilities'],
        d['total_assets']
    )

    d['x52'] = safe_divide(
        d['short_term_liabilities'] * 365,
        d['cost_of_products_sold']
    )

    d['x53'] = safe_divide(
        d['equity'],
        fixed_assets
    )

    d['x54'] = safe_divide(
        constant_capital,
        fixed_assets
    )

    d['x55'] = working_capital

    d['x56'] = safe_divide(
        (
            d['sales_revenue']
            - d['cost_of_products_sold']
        ),
        d['sales_revenue']
    )

    d['x57'] = safe_divide(
        (
            d['current_assets']
            - d['inventory']
            - d['short_term_liabilities']
        ),
        (
            d['sales_revenue']
            - d['gross_profit']
            - d['depreciation']
        )
    )

    d['x58'] = safe_divide(
        d['total_costs'],
        d['sales_revenue']
    )

    d['x59'] = safe_divide(
        long_term_liabilities,
        d['equity']
    )

    d['x60'] = safe_divide(
        d['sales_revenue'],
        d['inventory']
    )

    d['x61'] = safe_divide(
        d['sales_revenue'],
        d['receivables']
    )

    d['x62'] = safe_divide(
        d['short_term_liabilities'] * 365,
        d['sales_revenue']
    )

    d['x63'] = safe_divide(
        d['sales_revenue'],
        d['short_term_liabilities']
    )

    d['x64'] = safe_divide(
        d['sales_revenue'],
        fixed_assets
    )

    d['x65'] = d['x6'] / d['x2'].replace(0, 0.001)
    d['x66'] = d['x11'] / d['x3'].replace(0, 0.001)

    d = d.replace([np.inf, -np.inf], np.nan)
    d = d.fillna(0)

    return d

User = get_user_model()
def auto_assign_analyst(company):
    analysts = User.objects.filter(role='analyst').annotate(
        company_count=Count('assigned_companies')
    ).order_by('company_count')

    best_analyst = analysts.first()

    if best_analyst:
        company.analyst = best_analyst
        company.save()
        return True
    return False

def save_calculated_data(company, upload_instance, df_final):
    if upload_instance.status == 'approved':
        raise ValidationError('Acest fișier a fost deja procesat.')

    existing_months = {
        pd.Period(date, freq='M')
        for date in FinancialStatement.objects.filter(company=company)
        .values_list("reporting_date", flat=True)
    }

    uploaded_months = {
        pd.Period(date, freq='M')
        for date in df_final["reporting_date"].tolist()
    }

    duplicate_months = existing_months.intersection(uploaded_months)

    if duplicate_months:
        duplicate_months_str = ", ".join(
            [str(month) for month in sorted(duplicate_months)]
        )

        raise ValidationError(
            f"Fișierul conține luni deja existente în sistem: {duplicate_months_str}. "
            "Încarcă doar luni financiare noi."
        )

    with transaction.atomic():
        for _, row in df_final.iterrows():
            statement = FinancialStatement.objects.create(
                company=company,
                source_upload=upload_instance,
                reporting_date=row['reporting_date'],
                net_profit=row['net_profit'],
                ebit=row['ebit'],
                sales_revenue=row['sales_revenue'],
                depreciation=row['depreciation'],
                operating_expenses=row['operating_expenses'],
                total_assets=row['total_assets'],
                current_assets=row['current_assets'],
                inventory=row['inventory'],
                cash=row['cash'],
                total_liabilities=row['total_liabilities'],
                short_term_liabilities=row['short_term_liabilities'],
                equity=row['equity'],
                retained_earnings=row['retained_earnings'],
                short_term_securities=row['short_term_securities'],
                receivables=row['receivables'],
                gross_profit=row['gross_profit'],
                extraordinary_items=row['extraordinary_items'],
                financial_expenses=row['financial_expenses'],
                interest=row['interest'],
                share_capital=row['share_capital'],
                profit_on_operating_activities=row['profit_on_operating_activities'],
                gross_profit_3_years=row['gross_profit_3_years'],
                cost_of_products_sold=row['cost_of_products_sold'],
                profit_on_sales=row['profit_on_sales'],
                total_costs=row['total_costs'],
                previous_period_sales=row['previous_period_sales'],
            )

            kpi_data = {
                f'x{i}': float(row.get(f'x{i}', 0))
                for i in range(1, 67)
            }

            label, probability, shap_explanation = predict_risk(kpi_data)

            snapshot = KPISnapshot.objects.create(
                statement=statement,
                prediction_label=label,
                bankruptcy_probability=probability,
                feature_importance_data=shap_explanation,
                **kpi_data
            )

            BaseReport.objects.create(snapshot=snapshot)

        upload_instance.status = 'approved'
        upload_instance.processed_at = timezone.now()
        upload_instance.rejection_reason = None
        upload_instance.save()

        company.is_onboarded = True
        company.save()

        if not company.analyst:
            auto_assign_analyst(company)

def process_financial_upload(upload_instance):
    try:
        onboarding_needed = not upload_instance.company.is_onboarded
        df_raw = validate_and_parse_financial_excel(
            upload_instance.file.path,
            is_onboarding=onboarding_needed
        )

        df_kpi = calculate_kpis(df_raw)

        save_calculated_data(upload_instance.company, upload_instance, df_kpi)

        return True, "Procesare reusita!"

    except ValidationError as e:
        upload_instance.status = 'rejected'
        upload_instance.rejection_reason = str(e)
        upload_instance.processed_at = timezone.now()
        upload_instance.save()
        return False, str(e)

    except Exception as e:
        upload_instance.status = 'rejected'
        upload_instance.rejection_reason = f"Eroare sistem: {str(e)}"
        upload_instance.processed_at = timezone.now()
        upload_instance.save()
        print(f"DEBUG EROARE REALA: {str(e)}")
        import traceback
        traceback.print_exc()
        return False, "A intervenit o eroare tehnica neprevazuta"