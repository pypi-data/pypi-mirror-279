from enum import Enum

class ArtifactSortBy(str, Enum):
    ArtifactId = "artifactId",
    CreatedOn = "createdOn",
    ModifiedOn = "modifiedOn",
    ArtifactType = "artifactType",
    Name = "name",

