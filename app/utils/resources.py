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

class DictObj:
    """
        Convert dictionaries to Object
    """
    def __init__(self, in_dict:dict):
        assert isinstance(in_dict, dict)
        for key, val in in_dict.items():
            if isinstance(val, (list, tuple)):
               setattr(self, key, [DictObj(x) if isinstance(x, dict) else x for x in val])
            else:
               setattr(self, key, DictObj(val) if isinstance(val, dict) else val)