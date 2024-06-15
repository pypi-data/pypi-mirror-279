from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="PostBackOfficeEventDefinitionEmailSubscriptionBody")


@_attrs_define
class PostBackOfficeEventDefinitionEmailSubscriptionBody:
    """
    Attributes:
        id_contact (Union[Unset, Any]):  Example: any.
        ids_event_definition (Union[Unset, Any]):  Example: any.
    """

    id_contact: Union[Unset, Any] = UNSET
    ids_event_definition: Union[Unset, Any] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id_contact = self.id_contact

        ids_event_definition = self.ids_event_definition

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id_contact is not UNSET:
            field_dict["idContact"] = id_contact
        if ids_event_definition is not UNSET:
            field_dict["idsEventDefinition"] = ids_event_definition

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id_contact = d.pop("idContact", UNSET)

        ids_event_definition = d.pop("idsEventDefinition", UNSET)

        post_back_office_event_definition_email_subscription_body = cls(
            id_contact=id_contact,
            ids_event_definition=ids_event_definition,
        )

        post_back_office_event_definition_email_subscription_body.additional_properties = d
        return post_back_office_event_definition_email_subscription_body

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
