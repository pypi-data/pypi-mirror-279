from __future__ import annotations
from dataclasses import dataclass, field
from kiota_abstractions.base_request_builder import BaseRequestBuilder
from kiota_abstractions.get_path_parameters import get_path_parameters
from kiota_abstractions.method import Method
from kiota_abstractions.request_adapter import RequestAdapter
from kiota_abstractions.request_information import RequestInformation
from kiota_abstractions.request_option import RequestOption
from kiota_abstractions.serialization import Parsable, ParsableFactory
from typing import Any, Callable, Dict, List, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .....models.artifact_meta_data import ArtifactMetaData
    from .....models.editable_artifact_meta_data import EditableArtifactMetaData
    from .....models.error import Error
    from .branches.branches_request_builder import BranchesRequestBuilder
    from .rules.rules_request_builder import RulesRequestBuilder
    from .versions.versions_request_builder import VersionsRequestBuilder

class WithArtifactItemRequestBuilder(BaseRequestBuilder):
    """
    Manage a single artifact.
    """
    def __init__(self,request_adapter: RequestAdapter, path_parameters: Optional[Union[Dict[str, Any], str]] = None) -> None:
        """
        Instantiates a new WithArtifactItemRequestBuilder and sets the default values.
        param path_parameters: The raw url or the Url template parameters for the request.
        param request_adapter: The request adapter to use to execute the requests.
        Returns: None
        """
        super().__init__(request_adapter, "{+baseurl}/groups/{groupId}/artifacts/{artifactId}", path_parameters)
    
    async def delete(self,request_configuration: Optional[WithArtifactItemRequestBuilderDeleteRequestConfiguration] = None) -> None:
        """
        Deletes an artifact completely, resulting in all versions of the artifact also beingdeleted.  This may fail for one of the following reasons:* No artifact with the `artifactId` exists (HTTP error `404`)* A server error occurred (HTTP error `500`)
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: None
        """
        request_info = self.to_delete_request_information(
            request_configuration
        )
        from .....models.error import Error

        error_mapping: Dict[str, ParsableFactory] = {
            "404": Error,
            "500": Error,
        }
        if not self.request_adapter:
            raise Exception("Http core is null") 
        return await self.request_adapter.send_no_response_content_async(request_info, error_mapping)
    
    async def get(self,request_configuration: Optional[WithArtifactItemRequestBuilderGetRequestConfiguration] = None) -> Optional[ArtifactMetaData]:
        """
        Gets the metadata for an artifact in the registry, based on the latest version. If the latest version of the artifact is marked as `DISABLED`, the next available non-disabled version will be used. The returned metadata includesboth generated (read-only) and editable metadata (such as name and description).This operation can fail for the following reasons:* No artifact with this `artifactId` exists  or all versions are `DISABLED` (HTTP error `404`)* A server error occurred (HTTP error `500`)
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: Optional[ArtifactMetaData]
        """
        request_info = self.to_get_request_information(
            request_configuration
        )
        from .....models.error import Error

        error_mapping: Dict[str, ParsableFactory] = {
            "404": Error,
            "500": Error,
        }
        if not self.request_adapter:
            raise Exception("Http core is null") 
        from .....models.artifact_meta_data import ArtifactMetaData

        return await self.request_adapter.send_async(request_info, ArtifactMetaData, error_mapping)
    
    async def put(self,body: Optional[EditableArtifactMetaData] = None, request_configuration: Optional[WithArtifactItemRequestBuilderPutRequestConfiguration] = None) -> None:
        """
        Updates the editable parts of the artifact's metadata.  Not all metadata fields canbe updated.  Note that only the properties included will be updated.  You can updateonly the name by including only the `name` property in the payload of the request.Properties that are allowed but not present will result in the artifact's metadatanot being changed.This operation can fail for the following reasons:* No artifact with the `artifactId` exists (HTTP error `404`)* A server error occurred (HTTP error `500`)
        param body: The request body
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: None
        """
        if not body:
            raise TypeError("body cannot be null.")
        request_info = self.to_put_request_information(
            body, request_configuration
        )
        from .....models.error import Error

        error_mapping: Dict[str, ParsableFactory] = {
            "404": Error,
            "500": Error,
        }
        if not self.request_adapter:
            raise Exception("Http core is null") 
        return await self.request_adapter.send_no_response_content_async(request_info, error_mapping)
    
    def to_delete_request_information(self,request_configuration: Optional[WithArtifactItemRequestBuilderDeleteRequestConfiguration] = None) -> RequestInformation:
        """
        Deletes an artifact completely, resulting in all versions of the artifact also beingdeleted.  This may fail for one of the following reasons:* No artifact with the `artifactId` exists (HTTP error `404`)* A server error occurred (HTTP error `500`)
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: RequestInformation
        """
        request_info = RequestInformation()
        if request_configuration:
            request_info.headers.add_all(request_configuration.headers)
            request_info.add_request_options(request_configuration.options)
        request_info.url_template = self.url_template
        request_info.path_parameters = self.path_parameters
        request_info.http_method = Method.DELETE
        request_info.headers.try_add("Accept", "application/json")
        return request_info
    
    def to_get_request_information(self,request_configuration: Optional[WithArtifactItemRequestBuilderGetRequestConfiguration] = None) -> RequestInformation:
        """
        Gets the metadata for an artifact in the registry, based on the latest version. If the latest version of the artifact is marked as `DISABLED`, the next available non-disabled version will be used. The returned metadata includesboth generated (read-only) and editable metadata (such as name and description).This operation can fail for the following reasons:* No artifact with this `artifactId` exists  or all versions are `DISABLED` (HTTP error `404`)* A server error occurred (HTTP error `500`)
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: RequestInformation
        """
        request_info = RequestInformation()
        if request_configuration:
            request_info.headers.add_all(request_configuration.headers)
            request_info.add_request_options(request_configuration.options)
        request_info.url_template = self.url_template
        request_info.path_parameters = self.path_parameters
        request_info.http_method = Method.GET
        request_info.headers.try_add("Accept", "application/json")
        return request_info
    
    def to_put_request_information(self,body: Optional[EditableArtifactMetaData] = None, request_configuration: Optional[WithArtifactItemRequestBuilderPutRequestConfiguration] = None) -> RequestInformation:
        """
        Updates the editable parts of the artifact's metadata.  Not all metadata fields canbe updated.  Note that only the properties included will be updated.  You can updateonly the name by including only the `name` property in the payload of the request.Properties that are allowed but not present will result in the artifact's metadatanot being changed.This operation can fail for the following reasons:* No artifact with the `artifactId` exists (HTTP error `404`)* A server error occurred (HTTP error `500`)
        param body: The request body
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: RequestInformation
        """
        if not body:
            raise TypeError("body cannot be null.")
        request_info = RequestInformation()
        if request_configuration:
            request_info.headers.add_all(request_configuration.headers)
            request_info.add_request_options(request_configuration.options)
        request_info.url_template = self.url_template
        request_info.path_parameters = self.path_parameters
        request_info.http_method = Method.PUT
        request_info.headers.try_add("Accept", "application/json")
        request_info.set_content_from_parsable(self.request_adapter, "application/json", body)
        return request_info
    
    def with_url(self,raw_url: Optional[str] = None) -> WithArtifactItemRequestBuilder:
        """
        Returns a request builder with the provided arbitrary URL. Using this method means any other path or query parameters are ignored.
        param raw_url: The raw URL to use for the request builder.
        Returns: WithArtifactItemRequestBuilder
        """
        if not raw_url:
            raise TypeError("raw_url cannot be null.")
        return WithArtifactItemRequestBuilder(self.request_adapter, raw_url)
    
    @property
    def branches(self) -> BranchesRequestBuilder:
        """
        Manage branches of an artifact.
        """
        from .branches.branches_request_builder import BranchesRequestBuilder

        return BranchesRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def rules(self) -> RulesRequestBuilder:
        """
        Manage the rules for a single artifact.
        """
        from .rules.rules_request_builder import RulesRequestBuilder

        return RulesRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def versions(self) -> VersionsRequestBuilder:
        """
        Manage all the versions of an artifact in the registry.
        """
        from .versions.versions_request_builder import VersionsRequestBuilder

        return VersionsRequestBuilder(self.request_adapter, self.path_parameters)
    
    from kiota_abstractions.base_request_configuration import BaseRequestConfiguration

    @dataclass
    class WithArtifactItemRequestBuilderDeleteRequestConfiguration(BaseRequestConfiguration):
        from kiota_abstractions.base_request_configuration import BaseRequestConfiguration

        """
        Configuration for the request such as headers, query parameters, and middleware options.
        """
    
    from kiota_abstractions.base_request_configuration import BaseRequestConfiguration

    @dataclass
    class WithArtifactItemRequestBuilderGetRequestConfiguration(BaseRequestConfiguration):
        from kiota_abstractions.base_request_configuration import BaseRequestConfiguration

        """
        Configuration for the request such as headers, query parameters, and middleware options.
        """
    
    from kiota_abstractions.base_request_configuration import BaseRequestConfiguration

    @dataclass
    class WithArtifactItemRequestBuilderPutRequestConfiguration(BaseRequestConfiguration):
        from kiota_abstractions.base_request_configuration import BaseRequestConfiguration

        """
        Configuration for the request such as headers, query parameters, and middleware options.
        """
    

