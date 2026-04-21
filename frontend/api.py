import requests

BASE_URL = "http://127.0.0.1:8000/api"


def handle_response(response):
    try:
        data = response.json()
    except Exception:
        data = {"detail": "Răspuns invalid de la server."}

    if response.status_code >= 400:
        message = data.get("detail") or data.get("message") or str(data)
        return {"success": False, "message": message, "errors": data}

    return {"success": True, "data": data}


def auth_headers(access_token: str):
    return {
        "Authorization": f"Bearer {access_token}"
    }


def login_request(username: str, password: str):
    url = f"{BASE_URL}/token/"
    payload = {
        "username": username,
        "password": password,
    }

    try:
        response = requests.post(url, json=payload, timeout=10)
        result = handle_response(response)

        if result["success"]:
            return {
                "success": True,
                **result["data"]
            }

        return result

    except requests.RequestException:
        return {
            "success": False,
            "message": "Nu s-a putut realiza conexiunea cu backend-ul."
        }


def register_client(payload: dict):
    url = f"{BASE_URL}/register/client/"
    try:
        response = requests.post(url, json=payload, timeout=10)
        return handle_response(response)
    except requests.RequestException:
        return {
            "success": False,
            "message": "Nu s-a putut realiza conexiunea cu backend-ul."
        }


def register_analyst(payload: dict):
    url = f"{BASE_URL}/register/analyst/"
    try:
        response = requests.post(url, json=payload, timeout=10)
        return handle_response(response)
    except requests.RequestException:
        return {
            "success": False,
            "message": "Nu s-a putut realiza conexiunea cu backend-ul."
        }


def get_client_dashboard(company_id: int, access_token: str):
    url = f"{BASE_URL}/companies/{company_id}/dashboard/"
    try:
        response = requests.get(url, headers=auth_headers(access_token), timeout=10)
        return handle_response(response)
    except requests.RequestException:
        return {
            "success": False,
            "message": "Nu s-au putut încărca datele dashboard-ului client."
        }


def upload_financial_file(company_id: int, file, access_token: str):
    url = f"{BASE_URL}/uploads/"
    try:
        files = {
            "file": (file.name, file.getvalue(), file.type)
        }
        data = {
            "company_id": company_id
        }

        response = requests.post(
            url,
            headers=auth_headers(access_token),
            files=files,
            data=data,
            timeout=30
        )
        return handle_response(response)
    except requests.RequestException:
        return {
            "success": False,
            "message": "Fișierul nu a putut fi încărcat."
        }


def get_upload_history(company_id: int, access_token: str):
    url = f"{BASE_URL}/companies/{company_id}/uploads/"
    try:
        response = requests.get(url, headers=auth_headers(access_token), timeout=10)
        return handle_response(response)
    except requests.RequestException:
        return {
            "success": False,
            "message": "Istoricul importurilor nu a putut fi încărcat."
        }


def get_analyst_dashboard_stats(access_token: str):
    url = f"{BASE_URL}/analyst/dashboard-stats/"
    try:
        response = requests.get(url, headers=auth_headers(access_token), timeout=10)
        return handle_response(response)
    except requests.RequestException:
        return {
            "success": False,
            "message": "Nu s-au putut încărca statisticile analistului."
        }


def get_companies(access_token: str):
    url = f"{BASE_URL}/companies/"
    try:
        response = requests.get(url, headers=auth_headers(access_token), timeout=10)
        return handle_response(response)
    except requests.RequestException:
        return {
            "success": False,
            "message": "Lista companiilor nu a putut fi încărcată."
        }