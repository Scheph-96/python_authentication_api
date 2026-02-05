import structlog

def get_logger(name: str = None):
    return structlog.get_logger(name)