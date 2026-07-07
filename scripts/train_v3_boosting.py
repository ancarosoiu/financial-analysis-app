import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import shap
from scipy.io import arff
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score
import lightgbm as lgb
import joblib


def load_uci_data(folder_path):
    all_data = []

    for i in range(1, 6):
        file_name = f"{i}year.arff"
        file_path = os.path.join(folder_path, file_name)

        if os.path.exists(file_path):
            print(f"Se încarca {file_name}...")
            data, meta = arff.loadarff(file_path)
            df = pd.DataFrame(data)
            all_data.append(df)
        else:
            print(f"Fisierul {file_name} nu a fost gasit la calea {file_path}")

    if not all_data:
        raise FileNotFoundError("Nu s-a putut încarca niciun fișier .arff!")

    full_df = pd.concat(all_data, ignore_index=True)
    full_df['class'] = full_df['class'].str.decode('utf-8').astype(int)

    cols = {f'Attr{i}': f'x{i}' for i in range(1, 65)}
    full_df = full_df.rename(columns=cols)

    return full_df

def apply_feature_engineering(df):
    print("Facem feature engineering pentru x65 si x66...")
    df['x65'] = df['x6'] / df['x2'].replace(0, 0.001)
    df['x66'] = df['x11'] / df['x3'].replace(0, 0.001)

    df = df.replace([np.inf, -np.inf], np.nan)
    return df

def train_model():
    base_dir = os.getcwd()
    data_path = os.path.join(base_dir, 'backend', 'data', 'uci_polish_data')
    save_path = os.path.join(base_dir, 'backend', 'media', 'ml_models', 'boosted_polish_model_v3.joblib')
    scripts_path = os.path.join(base_dir, 'scripts')

    try:
        df = load_uci_data(data_path)
        df = apply_feature_engineering(df)
        print(f"Date încărcate. Total rânduri: {len(df)}")
    except Exception as e:
        print(f"Eroare la încărcare: {e}")
        return

    df = df.fillna(df.mean())

    X = df.drop(columns=['class'])
    y = df['class']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    print("Antrenam modelul LightGBM pentru 66 indicatori...")
    model = lgb.LGBMClassifier(
        n_estimators=1000,
        learning_rate=0.05,
        class_weight='balanced',
        random_state=42,
        n_jobs=-1
    )
    model.fit(X_train, y_train)

    print("Generam clasamentul indicatorilor...")
    importance = model.feature_importances_
    feat_importance = pd.DataFrame({
        'Indicator': X.columns,
        'Importance_Score': importance
    }).sort_values(by='Importance_Score', ascending=False)

    feat_importance['Rank'] = range(1, len(feat_importance) + 1)

    importance_csv_path = os.path.join(scripts_path, 'feature_importance_v3.csv')
    feat_importance.to_csv(importance_csv_path, index=False)
    print(f"CSV salvat: {importance_csv_path}")

    print("Generam analiza SHAP (poate dura cateva momente)...")
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X_test)

    if isinstance(shap_values, list):
        shap_to_plot = shap_values[1]
    else:
        shap_to_plot = shap_values

    plt.figure(figsize=(12, 10))
    shap.summary_plot(shap_to_plot, X_test, plot_type="bar", show=False)

    shap_plot_path = os.path.join(scripts_path, 'shap_summary_v3.png')
    plt.savefig(shap_plot_path, bbox_inches='tight')
    plt.close()
    print(f"Grafic SHAP salvat: {shap_plot_path}")

    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)

    print("-" * 30)
    print(f"PERFORMANTA MODEL:")
    print(f"Acuratete: {acc:.4f} (Cat de des ghicește corect)")
    print(f"F1-Score:  {f1:.4f} (Echilibrul intre precizie si identificarea falimentelor)")
    print("-" * 30)

    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    joblib.dump(model, save_path)
    print(f"Model salvat în: {save_path}")


if __name__ == "__main__":
    train_model()