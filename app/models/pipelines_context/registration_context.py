from app.models.pipelines_context.global_context import GlobalContext


class RegistrationContext(GlobalContext):
    def __init__(self, request_data):
        super().__init__(request_data)
        self.user = None