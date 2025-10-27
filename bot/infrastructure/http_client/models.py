from pydantic import BaseModel, ConfigDict

def to_camel(string: str) -> str:
    s = ''.join(word.capitalize() for word in string.split('_'))
    return s[0].lower() + s[1:]

class AppBaseModel(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True, arbitrary_types_allowed=True)

class ApiCamelModel(AppBaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True, alias_generator=to_camel)
