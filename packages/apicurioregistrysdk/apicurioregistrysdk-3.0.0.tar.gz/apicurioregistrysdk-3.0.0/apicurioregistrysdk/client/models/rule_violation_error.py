from __future__ import annotations
from dataclasses import dataclass, field
from kiota_abstractions.serialization import Parsable, ParseNode, SerializationWriter
from typing import Any, Callable, Dict, List, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .error import Error
    from .rule_violation_cause import RuleViolationCause

from .error import Error

@dataclass
class RuleViolationError(Error):
    """
    All error responses, whether `4xx` or `5xx` will include one of these as the responsebody.
    """
    # List of rule violation causes.
    causes: Optional[List[RuleViolationCause]] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: Optional[ParseNode] = None) -> RuleViolationError:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: RuleViolationError
        """
        if not parse_node:
            raise TypeError("parse_node cannot be null.")
        return RuleViolationError()
    
    def get_field_deserializers(self,) -> Dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: Dict[str, Callable[[ParseNode], None]]
        """
        from .error import Error
        from .rule_violation_cause import RuleViolationCause

        from .error import Error
        from .rule_violation_cause import RuleViolationCause

        fields: Dict[str, Callable[[Any], None]] = {
            "causes": lambda n : setattr(self, 'causes', n.get_collection_of_object_values(RuleViolationCause)),
        }
        super_fields = super().get_field_deserializers()
        fields.update(super_fields)
        return fields
    
    def serialize(self,writer: SerializationWriter) -> None:
        """
        Serializes information the current object
        param writer: Serialization writer to use to serialize this model
        Returns: None
        """
        if not writer:
            raise TypeError("writer cannot be null.")
        super().serialize(writer)
        writer.write_collection_of_object_values("causes", self.causes)
    

