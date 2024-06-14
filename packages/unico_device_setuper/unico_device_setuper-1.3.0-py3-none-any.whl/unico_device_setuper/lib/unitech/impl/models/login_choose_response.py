from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.login_choose_response_type import LoginChooseResponseType

if TYPE_CHECKING:
    from ..models.login_choose_response_clients_item import LoginChooseResponseClientsItem


T = TypeVar("T", bound="LoginChooseResponse")


@_attrs_define
class LoginChooseResponse:
    """
    Attributes:
        type (LoginChooseResponseType):
        clients (List['LoginChooseResponseClientsItem']):
    """

    type: LoginChooseResponseType
    clients: List["LoginChooseResponseClientsItem"]
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        type = self.type.value

        clients = []
        for clients_item_data in self.clients:
            clients_item = clients_item_data.to_dict()
            clients.append(clients_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type,
                "clients": clients,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.login_choose_response_clients_item import LoginChooseResponseClientsItem

        d = src_dict.copy()
        type = LoginChooseResponseType(d.pop("type"))

        clients = []
        _clients = d.pop("clients")
        for clients_item_data in _clients:
            clients_item = LoginChooseResponseClientsItem.from_dict(clients_item_data)

            clients.append(clients_item)

        login_choose_response = cls(
            type=type,
            clients=clients,
        )

        login_choose_response.additional_properties = d
        return login_choose_response

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
