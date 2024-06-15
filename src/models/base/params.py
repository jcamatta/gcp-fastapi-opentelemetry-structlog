from pydantic import BaseModel

class CustomBaseModel(BaseModel):

    def _common_str_repr(self) -> str:
        properties = []
        for name, value in self.__dict__.items():
            property_str = f"{name}({type(value).__name__})={value}"
            properties.append(property_str)
        properties_str = ", ".join(properties)
        return f"{type(self).__name__}({properties_str})"

    def __str__(self) -> str:
        return self._common_str_repr()
    
    def __repr__(self) -> str:
        return self._common_str_repr()


class Params(CustomBaseModel):
    bucket_name: str
    blob_name: str

    