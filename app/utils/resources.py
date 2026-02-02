import random

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
    code = ""
    for i in range(6):
        value = str(random.randrange(1, 10))
        code += value
    return code