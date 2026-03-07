# Pipelines

## What is a Pipeline?

A pipeline is all the steps that the system has to go through to finish a task, like user registration.
Those steps can be labeled as features.

In the registration process the steps are:
- User Creation (Password hashing and database insertion)
- Email Validation (Send a validation code to user email address)
- Role Assignment (assign default role to user)

These steps (features) constitute **Registration Pipeline**.

Depending on the use, a step can be enabled or disabled. Some steps are mandatory,
like 'User Creation'. Others can be enabled or disabled in [settings](../app/core/config.py)

## Where are pipelines built?

Pipelines are built in [factories](../app/core/factories).

[Authentication_Factory](../app/core/factories/authentication_factory.py) contains pipeline builders for authentication tasks.
The factory build a list of enabled steps that have to be executed for the task, then [TaskPipeline](../app/services/Infrastructure/task_pipeline.py) 
receive the list and run each step.

## How to use?

The builder is called in its task service, like registration pipeline builder is called in authentication [service](../app/services/core_services/authentication/authentication_service.py).
Steps are located [here](../app/services/core_services/authentication/pipelines) and each step does a specific operation.
