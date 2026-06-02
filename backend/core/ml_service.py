import os
import joblib
import pandas as pd
import numpy as np
import shap
from .models import MLModelVersion
from django.conf import settings
from django.core.exceptions import ValidationError


def get_trained_model():
    active_model = MLModelVersion.objects.filter(is_active=True).first()

    if not active_model:
        raise ValidationError(
            "Nu a fost găsit niciun model ML activ în baza de date."
        )

    model_path = os.path.join(settings.MEDIA_ROOT, active_model.file_path)

    if not os.path.exists(model_path):
        raise ValidationError(
            f"Fișierul modelului ML activ nu există la calea configurată: {model_path}"
        )

    try:
        model = joblib.load(model_path)
    except Exception as exc:
        raise ValidationError(
            f"Modelul ML activ nu a putut fi încărcat: {str(exc)}"
        )

    return model


def _safe_divide(numerator, denominator):
    numerator = float(numerator or 0)
    denominator = float(denominator or 0)

    if denominator == 0:
        return 0.0

    return numerator / denominator


def extract_local_shap_values(model, data_table):
    try:
        explainer = shap.TreeExplainer(model)
        shap_values = explainer.shap_values(data_table)

        if isinstance(shap_values, list):
            class_index = 1 if len(shap_values) > 1 else 0
            local_values = np.asarray(shap_values[class_index])[0]

        else:
            shap_array = np.asarray(shap_values)

            if shap_array.ndim == 2:
                local_values = shap_array[0]

            elif shap_array.ndim == 3:
                class_index = 1 if shap_array.shape[2] > 1 else 0
                local_values = shap_array[0, :, class_index]

            else:
                raise ValidationError(
                    "Formatul valorilor SHAP nu este compatibil cu predicția locală."
                )

        expected_value = np.asarray(explainer.expected_value).flatten()

        if expected_value.size > 1:
            base_value = float(expected_value[1])
        else:
            base_value = float(expected_value[0])

        return local_values, base_value

    except ValidationError:
        raise

    except Exception as exc:
        raise ValidationError(
            f"Explicația SHAP locală nu a putut fi calculată: {str(exc)}"
        )


def predict_risk(data_dict):
    model = get_trained_model()

    local_columns = [f"x{i}" for i in range(1, 67)]

    try:
        clean_data = {
            column: float(data_dict.get(column, 0) or 0)
            for column in local_columns
        }

        if "x65" not in data_dict:
            clean_data["x65"] = _safe_divide(
                clean_data.get("x6", 0),
                clean_data.get("x2", 0)
            )

        if "x66" not in data_dict:
            clean_data["x66"] = _safe_divide(
                clean_data.get("x11", 0),
                clean_data.get("x3", 0)
            )

    except (ValueError, TypeError) as exc:
        raise ValidationError(
            f"Indicatorii KPI nu au putut fi convertiți numeric pentru predicție: {str(exc)}"
        )

    data_table = pd.DataFrame([clean_data], columns=local_columns)
    data_table = data_table.replace([np.inf, -np.inf], np.nan).fillna(0)

    model_features = list(getattr(model, "feature_name_", []))

    if model_features and model_features != local_columns:
        raise ValidationError(
            "Modelul ML activ nu este compatibil cu indicatorii X1-X66 trimiși de aplicație."
        )

    try:
        model_result = int(model.predict(data_table)[0])
        model_probability = float(model.predict_proba(data_table)[0][1])
    except Exception as exc:
        raise ValidationError(
            f"Predicția ML nu a putut fi generată: {str(exc)}"
        )

    model_percentage = round(model_probability * 100, 2)

    local_shap_values, base_value = extract_local_shap_values(
        model,
        data_table
    )

    factor_rows = []

    for indicator, shap_value in zip(local_columns, local_shap_values):
        shap_value = float(shap_value)
        feature_value = float(data_table.iloc[0][indicator])

        if shap_value > 0:
            direction = "increase_risk"
        elif shap_value < 0:
            direction = "reduce_risk"
        else:
            direction = "neutral"

        factor_rows.append({
            "indicator": indicator,
            "feature_value": round(feature_value, 6),
            "shap_value": round(shap_value, 6),
            "absolute_impact": round(abs(shap_value), 6),
            "direction": direction,
        })

    top_factors = sorted(
        factor_rows,
        key=lambda item: item["absolute_impact"],
        reverse=True
    )[:5]

    risk_factors = sorted(
        [
            item for item in factor_rows
            if item["direction"] == "increase_risk"
        ],
        key=lambda item: item["shap_value"],
        reverse=True
    )[:5]

    protective_factors = sorted(
        [
            item for item in factor_rows
            if item["direction"] == "reduce_risk"
        ],
        key=lambda item: abs(item["shap_value"]),
        reverse=True
    )[:5]

    shap_explanation = {
        "method": "local_shap",
        "explained_class": "FALIMENT",
        "output_unit": "raw_score",
        "base_value": round(base_value, 6),
        "predicted_probability": model_percentage,
        "top_factors": top_factors,
        "risk_factors": risk_factors,
        "protective_factors": protective_factors,
    }

    label = "FALIMENT" if model_result == 1 else "STABIL"

    return label, model_percentage, shap_explanation