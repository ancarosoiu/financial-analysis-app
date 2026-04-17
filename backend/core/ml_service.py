import joblib
import os
import pandas as pd
from django.conf import settings
from .models import MLModelVersion

#functie prin care se extrage din path fisierul binar si este incarcat in memorie ca obiect de tip model
def get_trained_model():
    active_model = MLModelVersion.objects.filter(is_active=True).first()

    if not active_model:
        return None, "Nu a fost gasit niciun model activ in baza de date"

    path = os.path.join(settings.MEDIA_ROOT, active_model.file_path)

    model = joblib.load(path)
    return model, None

def predict_risk(data_dict):
    model, error = get_trained_model()

    if error:
        print(error)
        return "A fost detectata o eroare la preluarea modelului antrenat", 0.0, {}

    try:
        clean_data = {k: float(v) for k, v in data_dict.items() if k.startswith('x')}
        clean_data['x65'] = clean_data.get('x6', 0) / clean_data.get('x2', 0.001)
        clean_data['x66'] = clean_data.get('x11', 0) / clean_data.get('x3', 0.001)

    except (ValueError, TypeError, ZeroDivisionError):
        clean_data['x65'] = 0.0
        clean_data['x66'] = 0.0

    local_columns = [f'x{i}' for i in range(1, 67)]

    data_table = pd.DataFrame([clean_data], columns=local_columns).fillna(0)

    model_result = model.predict(data_table)[0]
    model_prob = model.predict_proba(data_table)[0][1]
    model_percentage = round(model_prob * 100, 2)

    importances = model.feature_importances_
    feature_map = list(zip(local_columns, importances))
    top_features = sorted(feature_map, key=lambda x: x[1], reverse=True)[:5]
    importance_dict = {name: round(float(imp), 4) for name, imp in top_features}

    label = "FALIMENT" if model_result == 1 else "STABIL"

    return label, model_percentage, importance_dict