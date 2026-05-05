from app.utils.resources import DictObj


class GlobalContext:
    def __init__(self, request_data):
        self.request_data = DictObj(request_data)