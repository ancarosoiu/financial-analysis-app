import os
import pandas as pd
import numpy as np
import joblib
from scipy.io import arff
import lightgbm as lgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score, f1_score
import shap
import matplotlib.pyplot as plt

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR,'backend', 'data', 'uci_polish_data')
MODEL_SAVE_PATH = os.path.join(BASE_DIR,'backend', 'media', 'ml_models')

def load_all_years():
    dfs = []
    for i in range(1, 6):
        file_path = os.path.join(DATA_PATH, f"{i}year.arff")
        data, _ = arff.loadarff(file_path)
        dfs.append(pd.DataFrame(data))
    return pd.concat(dfs, ignore_index=True)

print("Se incarca datele UCI...")
df = load_all_years()
df['class'] = df['class'].astype(int)
df.columns = [col.replace('Attr', 'x') if 'Attr' in col else col for col in df.columns]

df['x65'] = df['x6'] / df['x2']
df = df.replace([np.inf, -np.inf], np.nan).fillna(df.median())

X = df.drop('class', axis=1)
y = df['class']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

print("Antrenare LightGBM...")
model = lgb.LGBMClassifier(n_estimators=1000, learning_rate=0.05, class_weight='balanced', random_state=42)
model.fit(X_train, y_train)

os.makedirs(MODEL_SAVE_PATH, exist_ok=True)
model_filename = 'boosted_polish_model_v2.joblib'
joblib.dump(model, os.path.join(MODEL_SAVE_PATH, model_filename))

importance_df = pd.DataFrame({
    'feature': X.columns,
    'importance': model.feature_importances_
}).sort_values(by='importance', ascending=False)

importance_df.to_csv(os.path.join(BASE_DIR, 'scripts', 'feature_importance_v2.csv'), index=False)
print("CSV-ul pentru Streamlit a fost generat.")

print("Generare analiza SHAP...")
explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X_test)
joblib.dump(shap_values, os.path.join(MODEL_SAVE_PATH, 'shap_values_v2.joblib'))

print(f"Analiza AUC: {roc_auc_score(y_test, model.predict_proba(X_test)[:, 1]):.4f}")