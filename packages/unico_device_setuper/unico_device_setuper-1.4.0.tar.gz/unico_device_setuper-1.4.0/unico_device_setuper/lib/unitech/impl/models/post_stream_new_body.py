from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="PostStreamNewBody")


@_attrs_define
class PostStreamNewBody:
    """
    Attributes:
        label (Union[Unset, Any]):  Example: any.
        color (Union[Unset, Any]):  Example: any.
        volumic_mass (Union[Unset, Any]):  Example: any.
        operation_code (Union[Unset, Any]):  Example: any.
        track_dechet_waste_stream_id (Union[Unset, Any]):  Example: any.
        logo_url (Union[Unset, Any]):  Example: any.
    """

    label: Union[Unset, Any] = UNSET
    color: Union[Unset, Any] = UNSET
    volumic_mass: Union[Unset, Any] = UNSET
    operation_code: Union[Unset, Any] = UNSET
    track_dechet_waste_stream_id: Union[Unset, Any] = UNSET
    logo_url: Union[Unset, Any] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        label = self.label

        color = self.color

        volumic_mass = self.volumic_mass

        operation_code = self.operation_code

        track_dechet_waste_stream_id = self.track_dechet_waste_stream_id

        logo_url = self.logo_url

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if label is not UNSET:
            field_dict["label"] = label
        if color is not UNSET:
            field_dict["color"] = color
        if volumic_mass is not UNSET:
            field_dict["volumicMass"] = volumic_mass
        if operation_code is not UNSET:
            field_dict["operationCode"] = operation_code
        if track_dechet_waste_stream_id is not UNSET:
            field_dict["trackDechetWasteStreamId"] = track_dechet_waste_stream_id
        if logo_url is not UNSET:
            field_dict["logoUrl"] = logo_url

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        label = d.pop("label", UNSET)

        color = d.pop("color", UNSET)

        volumic_mass = d.pop("volumicMass", UNSET)

        operation_code = d.pop("operationCode", UNSET)

        track_dechet_waste_stream_id = d.pop("trackDechetWasteStreamId", UNSET)

        logo_url = d.pop("logoUrl", UNSET)

        post_stream_new_body = cls(
            label=label,
            color=color,
            volumic_mass=volumic_mass,
            operation_code=operation_code,
            track_dechet_waste_stream_id=track_dechet_waste_stream_id,
            logo_url=logo_url,
        )

        post_stream_new_body.additional_properties = d
        return post_stream_new_body

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
