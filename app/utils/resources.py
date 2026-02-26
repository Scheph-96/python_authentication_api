import secrets

def api_response(success, data=None, message="Success"):
    """
        Api response structure
    """
    return {
        "success": success,
        "message": message,
        "data": data
    }

def code_generator():
    """
        Generate 6 digit code for email validation
    """
    return f"{secrets.randbelow(1_000_000):06}"