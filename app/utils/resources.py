import secrets

"""
    Api response structure
"""
def api_response(success, data=None, message="Success"):
    return {
        "success": success,
        "message": message,
        "data": data
    }
    
"""
    Generate 6 digit code for email validation
"""
def code_generator():
    return f"{secrets.randbelow(1_000_000):06}"