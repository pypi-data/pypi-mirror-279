from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="PostCompanyLinkProducingPlacesBody")


@_attrs_define
class PostCompanyLinkProducingPlacesBody:
    """
    Attributes:
        producing_places (Union[Unset, Any]):  Example: any.
        id_company (Union[Unset, Any]):  Example: any.
    """

    producing_places: Union[Unset, Any] = UNSET
    id_company: Union[Unset, Any] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        producing_places = self.producing_places

        id_company = self.id_company

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if producing_places is not UNSET:
            field_dict["producingPlaces"] = producing_places
        if id_company is not UNSET:
            field_dict["idCompany"] = id_company

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        producing_places = d.pop("producingPlaces", UNSET)

        id_company = d.pop("idCompany", UNSET)

        post_company_link_producing_places_body = cls(
            producing_places=producing_places,
            id_company=id_company,
        )

        post_company_link_producing_places_body.additional_properties = d
        return post_company_link_producing_places_body

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
