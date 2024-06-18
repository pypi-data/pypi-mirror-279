from enum import Enum

class VersionSortBy(str, Enum):
    Version = "version",
    Name = "name",
    CreatedOn = "createdOn",
    ModifiedOn = "modifiedOn",
    GlobalId = "globalId",

