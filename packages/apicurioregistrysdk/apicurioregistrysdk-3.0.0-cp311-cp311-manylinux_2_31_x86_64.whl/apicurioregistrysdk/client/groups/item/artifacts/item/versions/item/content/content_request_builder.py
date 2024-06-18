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
    from ........models.error import Error
    from ........models.handle_references_type import HandleReferencesType

class ContentRequestBuilder(BaseRequestBuilder):
    """
    Manage a single version of a single artifact in the registry.
    """
    def __init__(self,request_adapter: RequestAdapter, path_parameters: Optional[Union[Dict[str, Any], str]] = None) -> None:
        """
        Instantiates a new ContentRequestBuilder and sets the default values.
        param path_parameters: The raw url or the Url template parameters for the request.
        param request_adapter: The request adapter to use to execute the requests.
        Returns: None
        """
        super().__init__(request_adapter, "{+baseurl}/groups/{groupId}/artifacts/{artifactId}/versions/{versionExpression}/content{?references*}", path_parameters)
    
    async def get(self,request_configuration: Optional[ContentRequestBuilderGetRequestConfiguration] = None) -> bytes:
        """
        Retrieves a single version of the artifact content.  Both the `artifactId` and theunique `version` number must be provided.  The `Content-Type` of the response depends on the artifact type.  In most cases, this is `application/json`, but for some types it may be different (for example, `PROTOBUF`).This operation can fail for the following reasons:* No artifact with this `artifactId` exists (HTTP error `404`)* No version with this `version` exists (HTTP error `404`)* A server error occurred (HTTP error `500`)
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: bytes
        """
        request_info = self.to_get_request_information(
            request_configuration
        )
        from ........models.error import Error

        error_mapping: Dict[str, ParsableFactory] = {
            "400": Error,
            "404": Error,
            "500": Error,
        }
        if not self.request_adapter:
            raise Exception("Http core is null") 
        return await self.request_adapter.send_primitive_async(request_info, "bytes", error_mapping)
    
    def to_get_request_information(self,request_configuration: Optional[ContentRequestBuilderGetRequestConfiguration] = None) -> RequestInformation:
        """
        Retrieves a single version of the artifact content.  Both the `artifactId` and theunique `version` number must be provided.  The `Content-Type` of the response depends on the artifact type.  In most cases, this is `application/json`, but for some types it may be different (for example, `PROTOBUF`).This operation can fail for the following reasons:* No artifact with this `artifactId` exists (HTTP error `404`)* No version with this `version` exists (HTTP error `404`)* A server error occurred (HTTP error `500`)
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: RequestInformation
        """
        request_info = RequestInformation()
        if request_configuration:
            request_info.headers.add_all(request_configuration.headers)
            request_info.set_query_string_parameters_from_raw_object(request_configuration.query_parameters)
            request_info.add_request_options(request_configuration.options)
        request_info.url_template = self.url_template
        request_info.path_parameters = self.path_parameters
        request_info.http_method = Method.GET
        request_info.headers.try_add("Accept", "*/*, application/json")
        return request_info
    
    def with_url(self,raw_url: Optional[str] = None) -> ContentRequestBuilder:
        """
        Returns a request builder with the provided arbitrary URL. Using this method means any other path or query parameters are ignored.
        param raw_url: The raw URL to use for the request builder.
        Returns: ContentRequestBuilder
        """
        if not raw_url:
            raise TypeError("raw_url cannot be null.")
        return ContentRequestBuilder(self.request_adapter, raw_url)
    
    @dataclass
    class ContentRequestBuilderGetQueryParameters():
        """
        Retrieves a single version of the artifact content.  Both the `artifactId` and theunique `version` number must be provided.  The `Content-Type` of the response depends on the artifact type.  In most cases, this is `application/json`, but for some types it may be different (for example, `PROTOBUF`).This operation can fail for the following reasons:* No artifact with this `artifactId` exists (HTTP error `404`)* No version with this `version` exists (HTTP error `404`)* A server error occurred (HTTP error `500`)
        """
        # Allows the user to specify how references in the content should be treated.
        references: Optional[HandleReferencesType] = None

    
    from kiota_abstractions.base_request_configuration import BaseRequestConfiguration

    @dataclass
    class ContentRequestBuilderGetRequestConfiguration(BaseRequestConfiguration):
        from kiota_abstractions.base_request_configuration import BaseRequestConfiguration

        """
        Configuration for the request such as headers, query parameters, and middleware options.
        """
        # Request query parameters
        query_parameters: Optional[ContentRequestBuilder.ContentRequestBuilderGetQueryParameters] = None

    

