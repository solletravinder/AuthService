from config import settings

def set_cookie(response, key, value, expires_minutes=None):
    domain = settings.COOKIE_DOMAIN
    secure = settings.COOKIE_SECURE.lower() == "true"
    is_local = domain in (None, "", "localhost", "127.0.0.1")
    GLOBAL_PATH = settings.GLOBAL_PATH

    cookie_params = {
        "httponly": True,
        "secure": secure if not is_local else False,
        "domain": domain if not is_local else None,
        "samesite": "lax",
    }
    if expires_minutes:
        from datetime import datetime, timedelta
        expire = datetime.utcnow() + timedelta(minutes=expires_minutes)
        cookie_params["expires"] = expire.strftime("%a, %d-%b-%Y %H:%M:%S GMT")

    response.set_cookie(key, value, **{k: v for k, v in cookie_params.items() if v is not None})
