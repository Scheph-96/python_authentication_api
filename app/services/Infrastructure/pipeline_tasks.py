class PipelineTasks:
    """
        Pipelines Tasks are all the steps that
        the system has to go through to finish a task
        like user registration. Those steps can be
        labeled as features.
    """
    def __init__(self, steps):
        self.steps = steps

    async def run(self, context):
        """
        Steps are executed one by one and each step return
        a context containing datas that is reused by the next
        step until the pipeline dry out.

        The final context containing user data and other
        values are returned to the service that launch
        the pipeline.

        :param context: Object containing requests data and users data
        :return: context
        """
        for step in self.steps:
            context = await step.run(context)
        return context