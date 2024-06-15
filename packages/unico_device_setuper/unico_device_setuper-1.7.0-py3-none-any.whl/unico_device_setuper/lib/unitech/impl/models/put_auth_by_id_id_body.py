from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="PutAuthByIdIdBody")


@_attrs_define
class PutAuthByIdIdBody:
    """
    Attributes:
        permissions (Union[Unset, Any]):  Example: any.
        firstname (Union[Unset, Any]):  Example: any.
        lastname (Union[Unset, Any]):  Example: any.
        sectors (Union[Unset, Any]):  Example: any.
    """

    permissions: Union[Unset, Any] = UNSET
    firstname: Union[Unset, Any] = UNSET
    lastname: Union[Unset, Any] = UNSET
    sectors: Union[Unset, Any] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        permissions = self.permissions

        firstname = self.firstname

        lastname = self.lastname

        sectors = self.sectors

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if permissions is not UNSET:
            field_dict["permissions"] = permissions
        if firstname is not UNSET:
            field_dict["firstname"] = firstname
        if lastname is not UNSET:
            field_dict["lastname"] = lastname
        if sectors is not UNSET:
            field_dict["sectors"] = sectors

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        permissions = d.pop("permissions", UNSET)

        firstname = d.pop("firstname", UNSET)

        lastname = d.pop("lastname", UNSET)

        sectors = d.pop("sectors", UNSET)

        put_auth_by_id_id_body = cls(
            permissions=permissions,
            firstname=firstname,
            lastname=lastname,
            sectors=sectors,
        )

        put_auth_by_id_id_body.additional_properties = d
        return put_auth_by_id_id_body

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
