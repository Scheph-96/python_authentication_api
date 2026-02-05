# Logging Workflow
lifespan() → configure logging engine
middleware → logs every request
exception handler → logs crashes
services → raise HTTPException

## Visual Architecture
                ┌────────────────────────┐
Request  ─────▶ │ FastAPI Router        │
                └──────────┬─────────────┘
                           │
                 HTTPException        Exception
                   (expected)         (unexpected)
                     │                    │
                     ▼                    ▼
        http_exception_handler   unhandled_exception_handler
             log.info()               log.error()
             return 4xx               return 500
