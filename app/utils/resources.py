import hashlib

"""
    Api response structure
"""
def api_response(success, data=None, message="Success"):
    return {
        "success": success,
        "message": message,
        "data": data
    }