from app.schemas.base_schema import BaseSchema
    

class EmailValidationCodeSubmit(BaseSchema):
    user_id: str
    code: str


class EmailValidationCodeRetry(BaseSchema):
    user_id: str
