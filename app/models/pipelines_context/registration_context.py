from app.utils.resources import DictObj


class RegistrationContext:
    def __init__(self, request_data):
        self.request_data = DictObj(request_data)
        self.user = None