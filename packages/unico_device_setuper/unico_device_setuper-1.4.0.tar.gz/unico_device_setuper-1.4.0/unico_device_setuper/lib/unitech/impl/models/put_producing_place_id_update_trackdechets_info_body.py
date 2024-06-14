from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="PutProducingPlaceIdUpdateTrackdechetsInfoBody")


@_attrs_define
class PutProducingPlaceIdUpdateTrackdechetsInfoBody:
    """
    Attributes:
        siret (Union[Unset, Any]):  Example: any.
        id (Union[Unset, Any]):  Example: any.
        address (Union[Unset, Any]):  Example: any.
        mail (Union[Unset, Any]):  Example: any.
        phone (Union[Unset, Any]):  Example: any.
        contact (Union[Unset, Any]):  Example: any.
        signature_code (Union[Unset, Any]):  Example: any.
    """

    siret: Union[Unset, Any] = UNSET
    id: Union[Unset, Any] = UNSET
    address: Union[Unset, Any] = UNSET
    mail: Union[Unset, Any] = UNSET
    phone: Union[Unset, Any] = UNSET
    contact: Union[Unset, Any] = UNSET
    signature_code: Union[Unset, Any] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        siret = self.siret

        id = self.id

        address = self.address

        mail = self.mail

        phone = self.phone

        contact = self.contact

        signature_code = self.signature_code

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if siret is not UNSET:
            field_dict["siret"] = siret
        if id is not UNSET:
            field_dict["id"] = id
        if address is not UNSET:
            field_dict["address"] = address
        if mail is not UNSET:
            field_dict["mail"] = mail
        if phone is not UNSET:
            field_dict["phone"] = phone
        if contact is not UNSET:
            field_dict["contact"] = contact
        if signature_code is not UNSET:
            field_dict["signatureCode"] = signature_code

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        siret = d.pop("siret", UNSET)

        id = d.pop("id", UNSET)

        address = d.pop("address", UNSET)

        mail = d.pop("mail", UNSET)

        phone = d.pop("phone", UNSET)

        contact = d.pop("contact", UNSET)

        signature_code = d.pop("signatureCode", UNSET)

        put_producing_place_id_update_trackdechets_info_body = cls(
            siret=siret,
            id=id,
            address=address,
            mail=mail,
            phone=phone,
            contact=contact,
            signature_code=signature_code,
        )

        put_producing_place_id_update_trackdechets_info_body.additional_properties = d
        return put_producing_place_id_update_trackdechets_info_body

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
