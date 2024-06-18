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
    from ....models.artifact_type_info import ArtifactTypeInfo
    from ....models.error import Error

class ArtifactTypesRequestBuilder(BaseRequestBuilder):
    """
    The list of artifact types supported by this instance of Registry.
    """
    def __init__(self,request_adapter: RequestAdapter, path_parameters: Optional[Union[Dict[str, Any], str]] = None) -> None:
        """
        Instantiates a new ArtifactTypesRequestBuilder and sets the default values.
        param path_parameters: The raw url or the Url template parameters for the request.
        param request_adapter: The request adapter to use to execute the requests.
        Returns: None
        """
        super().__init__(request_adapter, "{+baseurl}/admin/config/artifactTypes", path_parameters)
    
    async def get(self,request_configuration: Optional[ArtifactTypesRequestBuilderGetRequestConfiguration] = None) -> Optional[List[ArtifactTypeInfo]]:
        """
        Gets a list of all the configured artifact types.This operation can fail for the following reasons:* A server error occurred (HTTP error `500`)
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: Optional[List[ArtifactTypeInfo]]
        """
        request_info = self.to_get_request_information(
            request_configuration
        )
        from ....models.error import Error

        error_mapping: Dict[str, ParsableFactory] = {
            "500": Error,
        }
        if not self.request_adapter:
            raise Exception("Http core is null") 
        from ....models.artifact_type_info import ArtifactTypeInfo

        return await self.request_adapter.send_collection_async(request_info, ArtifactTypeInfo, error_mapping)
    
    def to_get_request_information(self,request_configuration: Optional[ArtifactTypesRequestBuilderGetRequestConfiguration] = None) -> RequestInformation:
        """
        Gets a list of all the configured artifact types.This operation can fail for the following reasons:* A server error occurred (HTTP error `500`)
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
    
    def with_url(self,raw_url: Optional[str] = None) -> ArtifactTypesRequestBuilder:
        """
        Returns a request builder with the provided arbitrary URL. Using this method means any other path or query parameters are ignored.
        param raw_url: The raw URL to use for the request builder.
        Returns: ArtifactTypesRequestBuilder
        """
        if not raw_url:
            raise TypeError("raw_url cannot be null.")
        return ArtifactTypesRequestBuilder(self.request_adapter, raw_url)
    
    from kiota_abstractions.base_request_configuration import BaseRequestConfiguration

    @dataclass
    class ArtifactTypesRequestBuilderGetRequestConfiguration(BaseRequestConfiguration):
        from kiota_abstractions.base_request_configuration import BaseRequestConfiguration

        """
        Configuration for the request such as headers, query parameters, and middleware options.
        """
    

