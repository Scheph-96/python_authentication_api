# Logging Workflow
```
lifespan() → configure logging engine
middleware → logs every request
exception handler → logs crashes
services → raise HTTPException
```

## Visual Architecture
```
                ┌────────────────────────┐
Request  ─────> │ FastAPI Router         │
                └──────────┬─────────────┘
                           │
                 HTTPException        Exception
                   (expected)         (unexpected)
                     │                    │
                     ▼                    ▼
        http_exception_handler   unhandled_exception_handler
             log.info()               log.error()
             return 4xx               return 500
```

## Structure
```
app/
 ├── core/
 │    ├──logging/
 │        ├── logging_config.py <!-- How log are displayed and structured
 │        └── logger.py <!-- Return a logger

app/
 ├── core/
 │    └── exception_config.py <!-- Configuration for HTTPExceptions and regular Exceptions

app/
 ├── middleware/
 │    └── middleware.py <!-- Perform logging on each request no matter the outcome
```