from app.models.dependencies_model.step import Step


class RoleAssignmentStep(Step):
    def __init__(self, role_service):
        self.role_service = role_service

    async def run(self, user):
        pass # Role assignment from role service