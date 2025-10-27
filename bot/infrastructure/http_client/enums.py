from enum import Enum

class RequestMethodType(str, Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"

class ClientsEnum(str, Enum):

    AI_HEALTH = "AI_HEALTH"
