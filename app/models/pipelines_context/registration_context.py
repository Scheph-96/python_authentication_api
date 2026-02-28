class RegistrationContext:
    def __init__(self, request_data):
        self.request_data = request_data
        self.user = None