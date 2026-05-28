# Financial Insight Pro

Aplicație web pentru **analiza financiară automată a companiilor** și **estimarea riscului de faliment** pe baza datelor financiare încărcate de utilizatori.

Platforma permite clienților să încarce situații financiare, să consulte indicatori calculați automat și să vizualizeze predicții de risc. Analiștii financiari pot valida importurile și pot completa rapoarte personalizate cu observații și recomandări.

---

## Funcționalități principale

### Client

- creare cont și autentificare;
- înregistrarea datelor companiei;
- încărcarea fișierelor Excel cu date financiare;
- consultarea statusului importurilor;
- vizualizarea dashboard-ului cu indicatori financiari;
- consultarea probabilității estimate de faliment;
- vizualizarea factorilor explicativi ai predicției;
- accesarea rapoartelor standard;
- solicitarea unui raport personalizat.

### Analist financiar

- autentificare într-o interfață dedicată;
- vizualizarea companiilor atribuite;
- aprobarea sau respingerea importurilor financiare;
- monitorizarea rezultatelor predictive;
- procesarea solicitărilor de raport personalizat;
- completarea observațiilor și recomandărilor pentru client.

---

## Tehnologii utilizate

| Componentă | Tehnologie |
|---|---|
| Frontend | Streamlit |
| Backend | Django, Django REST Framework |
| Autentificare | JWT / SimpleJWT |
| Bază de date | PostgreSQL |
| Containerizare | Docker Compose |
| Procesare date | Pandas, NumPy |
| Machine Learning | LightGBM |
| Interpretabilitate model | SHAP |
| Salvare model antrenat | Joblib |
| Date de intrare | Fișiere Excel |
| Rapoarte | PDF |

---

## Arhitectura aplicației

Aplicația este organizată pe o arhitectură de tip client–server:

```text
Browser web
    │
    ▼
Frontend Streamlit
    │
    │ REST API / JWT
    ▼
Backend Django REST Framework
    │
    ├── Autentificare și utilizatori
    ├── Gestionare companii
    ├── Import și validare date financiare
    ├── Calcul indicatori financiari
    ├── Predicție ML și explicații SHAP
    ├── Rapoarte și notificări
    │
    ├── PostgreSQL
    └── Fișiere media: Excel, model ML, rapoarte PDF
```

Frontend-ul oferă interfețe diferite pentru client și analist, iar backend-ul gestionează logica aplicației, validarea datelor, analiza financiară și comunicarea cu baza de date.

---

## Fluxul principal de funcționare

```text
Clientul încarcă datele financiare
        ↓
Sistemul verifică fișierul
        ↓
Analistul aprobă sau respinge importul
        ↓
Sistemul calculează indicatorii financiari
        ↓
Modelul ML estimează riscul de faliment
        ↓
SHAP explică rezultatul predicției
        ↓
Clientul consultă dashboard-ul și rapoartele
```

Predicția este realizată pentru fiecare perioadă financiară procesată, astfel încât evoluția riscului să poată fi analizată în timp.

---

## Structura proiectului

```text
licenta/
│
├── backend/
│   ├── config/              # Configurarea proiectului Django
│   ├── core/                # Modele, endpoint-uri și logică aplicație
│   ├── data/                # Date utilizate pentru modelul ML
│   ├── media/               # Fișiere încărcate, modele și rapoarte
│   ├── Dockerfile
│   ├── manage.py
│   └── requirements.txt
│
├── frontend/
│   ├── views/               # Interfețe Streamlit
│   ├── api.py               # Comunicare cu backend-ul
│   ├── app.py               # Pornirea aplicației frontend
│   ├── session.py           # Gestionarea sesiunii
│   └── requirements.txt
│
├── scripts/                 # Scripturi pentru antrenarea modelului
├── docker-compose.yml       # Backend Django și PostgreSQL
└── README.md
```

---

## Rularea aplicației local

### Cerințe

- Python 3
- Docker Desktop
- Git

### 1. Clonarea proiectului

```bash
git clone <repository-url>
cd licenta
```

### 2. Pornirea backend-ului și a bazei de date

Din rădăcina proiectului:

```bash
docker compose up --build
```

Backend-ul va fi disponibil la:

```text
http://localhost:8000
```

### 3. Pornirea frontend-ului

Într-un terminal separat:

```bash
cd frontend
pip install -r requirements.txt
streamlit run app.py
```

Interfața aplicației va fi disponibilă, de regulă, la:

```text
http://localhost:8501
```

---

## Model predictiv

Modelul de machine learning este antrenat separat pe date financiare istorice etichetate și este salvat în format `.joblib`.

Pentru datele noi aprobate în aplicație, sistemul:

1. calculează indicatorii financiari;
2. încarcă modelul activ;
3. generează clasificarea `STABIL` / `FALIMENT`;
4. calculează probabilitatea estimată de faliment;
5. furnizează explicații asupra predicției prin SHAP.

---

## Rapoarte

Aplicația oferă:

- **rapoarte standard**, generate pe baza indicatorilor și a predicției;
- **rapoarte personalizate**, solicitate de client și completate de analistul financiar cu observații și recomandări.

---

## Observație privind configurarea

Datele de conectare la baza de date și alte valori sensibile trebuie păstrate în variabile de mediu și nu trebuie publicate în repository.

---

## Autor

Proiect realizat în cadrul lucrării de licență, având ca obiectiv dezvoltarea unei platforme pentru analiza financiară automată și estimarea riscului de faliment al companiilor.
