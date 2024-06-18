from __future__ import annotations
from dataclasses import dataclass, field
from kiota_abstractions.serialization import AdditionalDataHolder, Parsable, ParseNode, SerializationWriter
from typing import Any, Callable, Dict, List, Optional, TYPE_CHECKING, Union

@dataclass
class UserInterfaceConfigFeatures(AdditionalDataHolder, Parsable):
    # Stores additional data not described in the OpenAPI description found when deserializing. Can be used for serialization as well.
    additional_data: Dict[str, Any] = field(default_factory=dict)

    # The breadcrumbs property
    breadcrumbs: Optional[bool] = None
    # The readOnly property
    read_only: Optional[bool] = None
    # The roleManagement property
    role_management: Optional[bool] = None
    # The settings property
    settings: Optional[bool] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: Optional[ParseNode] = None) -> UserInterfaceConfigFeatures:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: UserInterfaceConfigFeatures
        """
        if not parse_node:
            raise TypeError("parse_node cannot be null.")
        return UserInterfaceConfigFeatures()
    
    def get_field_deserializers(self,) -> Dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: Dict[str, Callable[[ParseNode], None]]
        """
        fields: Dict[str, Callable[[Any], None]] = {
            "breadcrumbs": lambda n : setattr(self, 'breadcrumbs', n.get_bool_value()),
            "readOnly": lambda n : setattr(self, 'read_only', n.get_bool_value()),
            "roleManagement": lambda n : setattr(self, 'role_management', n.get_bool_value()),
            "settings": lambda n : setattr(self, 'settings', n.get_bool_value()),
        }
        return fields
    
    def serialize(self,writer: SerializationWriter) -> None:
        """
        Serializes information the current object
        param writer: Serialization writer to use to serialize this model
        Returns: None
        """
        if not writer:
            raise TypeError("writer cannot be null.")
        writer.write_bool_value("breadcrumbs", self.breadcrumbs)
        writer.write_bool_value("readOnly", self.read_only)
        writer.write_bool_value("roleManagement", self.role_management)
        writer.write_bool_value("settings", self.settings)
        writer.write_additional_data_value(self.additional_data)
    

