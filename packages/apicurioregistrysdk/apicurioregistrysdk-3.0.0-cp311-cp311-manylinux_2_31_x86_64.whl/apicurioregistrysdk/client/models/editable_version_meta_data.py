from __future__ import annotations
from dataclasses import dataclass, field
from kiota_abstractions.serialization import AdditionalDataHolder, Parsable, ParseNode, SerializationWriter
from typing import Any, Callable, Dict, List, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .labels import Labels
    from .version_state import VersionState

@dataclass
class EditableVersionMetaData(AdditionalDataHolder, Parsable):
    # Stores additional data not described in the OpenAPI description found when deserializing. Can be used for serialization as well.
    additional_data: Dict[str, Any] = field(default_factory=dict)

    # The description property
    description: Optional[str] = None
    # User-defined name-value pairs. Name and value must be strings.
    labels: Optional[Labels] = None
    # The name property
    name: Optional[str] = None
    # Describes the state of an artifact or artifact version.  The following statesare possible:* ENABLED* DISABLED* DEPRECATED
    state: Optional[VersionState] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: Optional[ParseNode] = None) -> EditableVersionMetaData:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: EditableVersionMetaData
        """
        if not parse_node:
            raise TypeError("parse_node cannot be null.")
        return EditableVersionMetaData()
    
    def get_field_deserializers(self,) -> Dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: Dict[str, Callable[[ParseNode], None]]
        """
        from .labels import Labels
        from .version_state import VersionState

        from .labels import Labels
        from .version_state import VersionState

        fields: Dict[str, Callable[[Any], None]] = {
            "description": lambda n : setattr(self, 'description', n.get_str_value()),
            "labels": lambda n : setattr(self, 'labels', n.get_object_value(Labels)),
            "name": lambda n : setattr(self, 'name', n.get_str_value()),
            "state": lambda n : setattr(self, 'state', n.get_enum_value(VersionState)),
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
        writer.write_str_value("description", self.description)
        writer.write_object_value("labels", self.labels)
        writer.write_str_value("name", self.name)
        writer.write_enum_value("state", self.state)
        writer.write_additional_data_value(self.additional_data)
    

