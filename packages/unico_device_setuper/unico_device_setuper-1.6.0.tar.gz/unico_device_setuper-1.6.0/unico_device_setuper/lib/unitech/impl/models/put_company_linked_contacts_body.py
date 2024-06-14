from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="PutCompanyLinkedContactsBody")


@_attrs_define
class PutCompanyLinkedContactsBody:
    """
    Attributes:
        id_company (Union[Unset, Any]):  Example: any.
        ids_contact (Union[Unset, Any]):  Example: any.
    """

    id_company: Union[Unset, Any] = UNSET
    ids_contact: Union[Unset, Any] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id_company = self.id_company

        ids_contact = self.ids_contact

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id_company is not UNSET:
            field_dict["idCompany"] = id_company
        if ids_contact is not UNSET:
            field_dict["idsContact"] = ids_contact

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id_company = d.pop("idCompany", UNSET)

        ids_contact = d.pop("idsContact", UNSET)

        put_company_linked_contacts_body = cls(
            id_company=id_company,
            ids_contact=ids_contact,
        )

        put_company_linked_contacts_body.additional_properties = d
        return put_company_linked_contacts_body

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
