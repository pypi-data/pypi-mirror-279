# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from . import _utilities
from . import outputs
from ._inputs import *

__all__ = [
    'GetNetworkLinkEndpointResult',
    'AwaitableGetNetworkLinkEndpointResult',
    'get_network_link_endpoint',
    'get_network_link_endpoint_output',
]

@pulumi.output_type
class GetNetworkLinkEndpointResult:
    """
    A collection of values returned by getNetworkLinkEndpoint.
    """
    def __init__(__self__, description=None, display_name=None, environment=None, id=None, network_link_services=None, networks=None, resource_name=None):
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if display_name and not isinstance(display_name, str):
            raise TypeError("Expected argument 'display_name' to be a str")
        pulumi.set(__self__, "display_name", display_name)
        if environment and not isinstance(environment, dict):
            raise TypeError("Expected argument 'environment' to be a dict")
        pulumi.set(__self__, "environment", environment)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if network_link_services and not isinstance(network_link_services, list):
            raise TypeError("Expected argument 'network_link_services' to be a list")
        pulumi.set(__self__, "network_link_services", network_link_services)
        if networks and not isinstance(networks, list):
            raise TypeError("Expected argument 'networks' to be a list")
        pulumi.set(__self__, "networks", networks)
        if resource_name and not isinstance(resource_name, str):
            raise TypeError("Expected argument 'resource_name' to be a str")
        pulumi.set(__self__, "resource_name", resource_name)

    @property
    @pulumi.getter
    def description(self) -> str:
        """
        (Optional String) The description of the Network Link Endpoint.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> str:
        """
        (Optional String) The name of the Network Link Endpoint.
        """
        return pulumi.get(self, "display_name")

    @property
    @pulumi.getter
    def environment(self) -> 'outputs.GetNetworkLinkEndpointEnvironmentResult':
        return pulumi.get(self, "environment")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        (Required String) The ID of the Network Link Service
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="networkLinkServices")
    def network_link_services(self) -> Sequence['outputs.GetNetworkLinkEndpointNetworkLinkServiceResult']:
        """
        (Required Configuration Block) supports the following:
        """
        return pulumi.get(self, "network_link_services")

    @property
    @pulumi.getter
    def networks(self) -> Sequence['outputs.GetNetworkLinkEndpointNetworkResult']:
        """
        (Required Configuration Block) supports the following:
        """
        return pulumi.get(self, "networks")

    @property
    @pulumi.getter(name="resourceName")
    def resource_name(self) -> str:
        """
        (Required String) The Confluent Resource Name of the Network Link Endpoint.
        """
        return pulumi.get(self, "resource_name")


class AwaitableGetNetworkLinkEndpointResult(GetNetworkLinkEndpointResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetNetworkLinkEndpointResult(
            description=self.description,
            display_name=self.display_name,
            environment=self.environment,
            id=self.id,
            network_link_services=self.network_link_services,
            networks=self.networks,
            resource_name=self.resource_name)


def get_network_link_endpoint(environment: Optional[pulumi.InputType['GetNetworkLinkEndpointEnvironmentArgs']] = None,
                              id: Optional[str] = None,
                              opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetNetworkLinkEndpointResult:
    """
    [![General Availability](https://img.shields.io/badge/Lifecycle%20Stage-General%20Availability-%2345c6e8)](https://docs.confluent.io/cloud/current/api.html#section/Versioning/API-Lifecycle-Policy)

    `NetworkLinkEndpoint` describes a Network Link Endpoint data source.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_confluentcloud as confluentcloud

    nle = confluentcloud.get_network_link_endpoint(id="nle-1357",
        environment=confluentcloud.GetNetworkLinkEndpointEnvironmentArgs(
            id="env-1234",
        ))
    pulumi.export("networkLinkEndpoint", nle)
    ```


    :param str id: The ID of the Network Link Endpoint, for example, `nle-zyw30`.
    """
    __args__ = dict()
    __args__['environment'] = environment
    __args__['id'] = id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('confluentcloud:index/getNetworkLinkEndpoint:getNetworkLinkEndpoint', __args__, opts=opts, typ=GetNetworkLinkEndpointResult).value

    return AwaitableGetNetworkLinkEndpointResult(
        description=pulumi.get(__ret__, 'description'),
        display_name=pulumi.get(__ret__, 'display_name'),
        environment=pulumi.get(__ret__, 'environment'),
        id=pulumi.get(__ret__, 'id'),
        network_link_services=pulumi.get(__ret__, 'network_link_services'),
        networks=pulumi.get(__ret__, 'networks'),
        resource_name=pulumi.get(__ret__, 'resource_name'))


@_utilities.lift_output_func(get_network_link_endpoint)
def get_network_link_endpoint_output(environment: Optional[pulumi.Input[pulumi.InputType['GetNetworkLinkEndpointEnvironmentArgs']]] = None,
                                     id: Optional[pulumi.Input[str]] = None,
                                     opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetNetworkLinkEndpointResult]:
    """
    [![General Availability](https://img.shields.io/badge/Lifecycle%20Stage-General%20Availability-%2345c6e8)](https://docs.confluent.io/cloud/current/api.html#section/Versioning/API-Lifecycle-Policy)

    `NetworkLinkEndpoint` describes a Network Link Endpoint data source.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_confluentcloud as confluentcloud

    nle = confluentcloud.get_network_link_endpoint(id="nle-1357",
        environment=confluentcloud.GetNetworkLinkEndpointEnvironmentArgs(
            id="env-1234",
        ))
    pulumi.export("networkLinkEndpoint", nle)
    ```


    :param str id: The ID of the Network Link Endpoint, for example, `nle-zyw30`.
    """
    ...
