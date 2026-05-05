```.
├── app
│   ├── api
│   │   └── v1
│   │       ├── authentication_controller.py
│   │       └── authorization_controller.py
│   ├── core
│   │   ├── config.py
│   │   ├── errors
│   │   │   ├── authorization
│   │   │   │   └── authorization_errors.py
│   │   │   └── domain_errors.py
│   │   ├── exception_config.py
│   │   ├── factories
│   │   │   └── authentication_factory.py
│   │   └── logging
│   │       ├── logger.py
│   │       └── logging_config.py
│   ├── database
│   │   ├── db_motor.py
│   │   └── init_indexes.py
│   ├── keys
│   │   ├── private.pem
│   │   ├── private.pem.txt
│   │   ├── public.pem
│   │   └── public.pem.txt
│   ├── logs
│   │   └── app.log
│   ├── main.py
│   ├── middleware
│   │   └── logging_middleware.py
│   ├── models
│   │   ├── core_model
│   │   │   ├── authentication_model
│   │   │   │   ├── email_validation_code_model.py
│   │   │   │   ├── password_recovery_token_model.py
│   │   │   │   ├── refresh_token_model.py
│   │   │   │   └── user_model.py
│   │   │   └── authorization_model
│   │   │       ├── permission_model.py
│   │   │       ├── role_model.py
│   │   │       ├── role_permission_model.py
│   │   │       └── user_role_model.py
│   │   ├── dependencies_model
│   │   │   ├── authentication_dependencies.py
│   │   │   ├── authorization_dependencies.py
│   │   │   └── step.py
│   │   └── pipelines_context
│   │       ├── global_context.py
│   │       └── registration_context.py
│   ├── repositories
│   │   ├── authentication_repositories
│   │   │   ├── email_validation_code_repository.py
│   │   │   ├── password_recovery_token_repository.py
│   │   │   ├── refresh_token_repository.py
│   │   │   └── user_repository.py
│   │   ├── authorization_repositories
│   │   │   ├── permission_repository.py
│   │   │   ├── role_permission_repository.py
│   │   │   ├── role_repository.py
│   │   │   └── user_role_repository.py
│   │   └── base_repository.py
│   ├── schemas
│   │   ├── authentication_schemas
│   │   │   ├── email_validation_code_schema.py
│   │   │   ├── password_recovery_token_schema.py
│   │   │   ├── refresh_token_schema.py
│   │   │   └── user_schema.py
│   │   ├── authorization_schema
│   │   │   ├── permission_schema.py
│   │   │   └── role_schema.py
│   │   ├── base_schema.py
│   │   └── jwt_schema.py
│   ├── services
│   │   ├── core_services
│   │   │   ├── authentication
│   │   │   │   ├── authentication_service.py
│   │   │   │   ├── model_services
│   │   │   │   │   ├── email_validation_code_service.py
│   │   │   │   │   ├── password_recovery_token_service.py
│   │   │   │   │   ├── refresh_token_service.py
│   │   │   │   │   └── user_service.py
│   │   │   │   └── pipelines
│   │   │   │       └── registration_pipeline
│   │   │   │           └── steps
│   │   │   │               ├── assign_role_step.py
│   │   │   │               ├── email_validation_step.py
│   │   │   │               └── user_creation_step.py
│   │   │   └── authorization
│   │   │       ├── authorization_service.py
│   │   │       └── model_services
│   │   │           ├── permission_service.py
│   │   │           ├── role_permission_service.py
│   │   │           ├── role_service.py
│   │   │           └── user_role_service.py
│   │   └── Infrastructure
│   │       ├── email_service.py
│   │       └── pipeline_tasks.py
│   └── utils
│       ├── jwt.py
│       └── resources.py
├── docs
│   ├── authentication.md
│   ├── authorization.md
│   ├── database.md
│   ├── endpoints.md
│   ├── logging.md
│   ├── logout.md
│   ├── password_recovery.md
│   ├── pipeline.md
│   ├── project_filesystem.md
│   └── user_creation.md
├── .env
├── env.txt
├── .gitignore
├── launcher.py
├── README.md
└── requirements.txt

37 directories, 81 files
```