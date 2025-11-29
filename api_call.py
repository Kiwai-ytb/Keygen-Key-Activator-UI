import requests, os
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")
KEYGEN_TOKEN = os.getenv("KEYGEN_TOKEN")
PRODUCT_ID = os.getenv("KEYGEN_PRODUCT_ID")
ACCOUNT_ID = os.getenv("KEYGEN_ACCOUNT_ID")
POLICY_ID = os.getenv("KEYGEN_POLICY_ID")

def activate_key(license_key: str, machine_udid: str) -> dict:
    url_validate = f"https://api.keygen.sh/v1/accounts/{ACCOUNT_ID}/licenses/actions/validate-key"
    headers_json = {
        "Content-Type": "application/vnd.api+json",
        "Accept": "application/vnd.api+json"
    }
    data_validate = {
        "meta": {
            "key": license_key,
            "scope": {
                "policy": POLICY_ID
            }
        }
    }

    try:
        r = requests.post(url_validate, json=data_validate, headers=headers_json)
        if r.status_code != 200:
            return {
                "success": False,
                "error": f"Invalid or expired license key ({r.status_code}): {r.text}",
                "machine_id": None
            }

        validate_data = r.json()
        license_data = validate_data["data"]
        license_id = license_data["id"]
        license_name = license_data["attributes"].get("name", license_key)
    except Exception as e:
        return {"success": False, "error": str(e), "machine_id": None}

    url_machine = f"https://api.keygen.sh/v1/accounts/{ACCOUNT_ID}/machines"
    headers_auth = {
        "Authorization": f"Bearer {KEYGEN_TOKEN}",
        "Content-Type": "application/vnd.api+json",
        "Accept": "application/vnd.api+json"
    }
    data_machine = {
        "data": {
            "type": "machines",
            "attributes": {
                "fingerprint": machine_udid,
                "name": license_name
            },
            "relationships": {
                "license": {
                    "data": {
                        "type": "licenses",
                        "id": license_id
                    }
                }
            }
        }
    }

    try:
        r2 = requests.post(url_machine, json=data_machine, headers=headers_auth)
        resp = r2.json()
        if r2.status_code == 201:
            return {
                "success": True,
                "error": None,
                "machine_id": resp["data"]["id"],
                "status": r2.status_code
            }
        else:
            detail = resp.get("errors", [{}])[0].get("detail", "Activation failed")
            return {
                "success": False,
                "error": f"{detail} (status {r2.status_code})",
                "machine_id": None,
                "status": r2.status_code
            }
    except Exception as e:
        return {"success": False, "error": str(e), "machine_id": None}
