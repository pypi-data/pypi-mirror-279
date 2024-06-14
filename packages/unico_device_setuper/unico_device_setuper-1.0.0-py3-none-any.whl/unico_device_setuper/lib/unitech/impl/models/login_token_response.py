from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.login_token_response_type import LoginTokenResponseType

T = TypeVar("T", bound="LoginTokenResponse")


@_attrs_define
class LoginTokenResponse:
    """
    Attributes:
        type (LoginTokenResponseType):
        access_token (str):  Example: string.
    """

    type: LoginTokenResponseType
    access_token: str
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        type = self.type.value

        access_token = self.access_token

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type,
                "accessToken": access_token,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        type = LoginTokenResponseType(d.pop("type"))

        access_token = d.pop("accessToken")

        login_token_response = cls(
            type=type,
            access_token=access_token,
        )

        login_token_response.additional_properties = d
        return login_token_response

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
