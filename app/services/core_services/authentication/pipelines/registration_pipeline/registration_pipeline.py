class RegistrationPipeline:
    def __init__(self, steps):
        self.steps = steps

    async def run(self, context):
        for step in self.steps:
            context = await step.run(context)
        return context