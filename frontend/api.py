import requests

BASE_URL = "http://127.0.0.1:8000/api"


def handle_response(response):
    try:
        data = response.json()
    except Exception:
        data = {"detail": "Răspuns invalid de la server."}

    if response.status_code >= 400:
        message = (
                data.get("detail")
                or data.get("message")
                or data.get("error")
                or str(data)
        )
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

def create_company(payload: dict, access_token: str):
    url = f"{BASE_URL}/companies/"
    try:
        response = requests.post(
            url,
            json=payload,
            headers=auth_headers(access_token),
            timeout=10
        )
        return handle_response(response)
    except requests.RequestException:
        return {
            "success": False,
            "message": "Compania nu a putut fi creată."
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

def download_upload_file(upload_id: int, access_token: str):
    url = f"{BASE_URL}/uploads/{upload_id}/download/"

    try:
        response = requests.get(
            url,
            headers=auth_headers(access_token),
            timeout=30,
        )

        if response.status_code >= 400:
            try:
                data = response.json()
                message = (
                    data.get("detail")
                    or data.get("message")
                    or data.get("error")
                    or "Fișierul nu a putut fi descărcat."
                )
            except Exception:
                message = "Fișierul nu a putut fi descărcat."

            return {
                "success": False,
                "message": message,
            }

        return {
            "success": True,
            "content": response.content,
            "content_type": response.headers.get(
                "Content-Type",
                "application/octet-stream",
            ),
        }

    except requests.RequestException:
        return {
            "success": False,
            "message": "Nu s-a putut realiza descărcarea fișierului.",
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


def get_analyst_pending_uploads(access_token: str):
    url = f"{BASE_URL}/analyst/uploads/pending/"
    try:
        response = requests.get(
            url,
            headers=auth_headers(access_token),
            timeout=10
        )
        return handle_response(response)
    except requests.RequestException:
        return {
            "success": False,
            "message": "Importurile în așteptare nu au putut fi încărcate."
        }

def get_analyst_uploads(access_token: str, status: str = "pending"):
    url = f"{BASE_URL}/analyst/uploads/"
    params = {
        "status": status
    }

    try:
        response = requests.get(
            url,
            headers=auth_headers(access_token),
            params=params,
            timeout=10
        )
        return handle_response(response)
    except requests.RequestException:
        return {
            "success": False,
            "message": "Importurile nu au putut fi încărcate."
        }

def review_upload(upload_id: int, decision: str, access_token: str, reason: str = ""):
    url = f"{BASE_URL}/uploads/{upload_id}/review/"
    payload = {
        "decision": decision,
        "reason": reason,
    }

    try:
        response = requests.post(
            url,
            json=payload,
            headers=auth_headers(access_token),
            timeout=30
        )
        return handle_response(response)
    except requests.RequestException:
        return {
            "success": False,
            "message": "Importul nu a putut fi procesat."
        }