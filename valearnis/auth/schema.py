from ninja import Schema


class LoginSchema(Schema):
    email: str
    password: str


class AccessToken(Schema):
    access_token: str
