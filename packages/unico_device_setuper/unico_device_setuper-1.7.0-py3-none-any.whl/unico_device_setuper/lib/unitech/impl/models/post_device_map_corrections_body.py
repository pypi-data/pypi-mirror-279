from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="PostDeviceMapCorrectionsBody")


@_attrs_define
class PostDeviceMapCorrectionsBody:
    """
    Attributes:
        content_csv (Union[Unset, Any]):  Example: any.
    """

    content_csv: Union[Unset, Any] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        content_csv = self.content_csv

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if content_csv is not UNSET:
            field_dict["contentCsv"] = content_csv

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        content_csv = d.pop("contentCsv", UNSET)

        post_device_map_corrections_body = cls(
            content_csv=content_csv,
        )

        post_device_map_corrections_body.additional_properties = d
        return post_device_map_corrections_body

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
