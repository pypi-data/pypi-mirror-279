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

__all__ = [
    'GetByokKeyResult',
    'AwaitableGetByokKeyResult',
    'get_byok_key',
    'get_byok_key_output',
]

@pulumi.output_type
class GetByokKeyResult:
    """
    A collection of values returned by getByokKey.
    """
    def __init__(__self__, aws=None, azures=None, gcps=None, id=None):
        if aws and not isinstance(aws, list):
            raise TypeError("Expected argument 'aws' to be a list")
        pulumi.set(__self__, "aws", aws)
        if azures and not isinstance(azures, list):
            raise TypeError("Expected argument 'azures' to be a list")
        pulumi.set(__self__, "azures", azures)
        if gcps and not isinstance(gcps, list):
            raise TypeError("Expected argument 'gcps' to be a list")
        pulumi.set(__self__, "gcps", gcps)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)

    @property
    @pulumi.getter
    def aws(self) -> Sequence['outputs.GetByokKeyAwResult']:
        """
        (Optional Configuration Block) supports the following:
        """
        return pulumi.get(self, "aws")

    @property
    @pulumi.getter
    def azures(self) -> Sequence['outputs.GetByokKeyAzureResult']:
        """
        (Optional Configuration Block) supports the following:
        """
        return pulumi.get(self, "azures")

    @property
    @pulumi.getter
    def gcps(self) -> Sequence['outputs.GetByokKeyGcpResult']:
        """
        (Optional Configuration Block) supports the following:
        """
        return pulumi.get(self, "gcps")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        (Required String) The ID of the BYOK key, for example, `cck-abcde`.
        """
        return pulumi.get(self, "id")


class AwaitableGetByokKeyResult(GetByokKeyResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetByokKeyResult(
            aws=self.aws,
            azures=self.azures,
            gcps=self.gcps,
            id=self.id)


def get_byok_key(id: Optional[str] = None,
                 opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetByokKeyResult:
    """
    [![General Availability](https://img.shields.io/badge/Lifecycle%20Stage-General%20Availability-%2345c6e8)](https://docs.confluent.io/cloud/current/api.html#section/Versioning/API-Lifecycle-Policy)

    `ByokKey` describes a BYOK Key data source.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_confluentcloud as confluentcloud

    azure_key = confluentcloud.get_byok_key(id="cck-abcde")
    pulumi.export("byok", azure_key)
    ```


    :param str id: The ID of the BYOK key, for example, `cck-abcde`.
    """
    __args__ = dict()
    __args__['id'] = id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('confluentcloud:index/getByokKey:getByokKey', __args__, opts=opts, typ=GetByokKeyResult).value

    return AwaitableGetByokKeyResult(
        aws=pulumi.get(__ret__, 'aws'),
        azures=pulumi.get(__ret__, 'azures'),
        gcps=pulumi.get(__ret__, 'gcps'),
        id=pulumi.get(__ret__, 'id'))


@_utilities.lift_output_func(get_byok_key)
def get_byok_key_output(id: Optional[pulumi.Input[str]] = None,
                        opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetByokKeyResult]:
    """
    [![General Availability](https://img.shields.io/badge/Lifecycle%20Stage-General%20Availability-%2345c6e8)](https://docs.confluent.io/cloud/current/api.html#section/Versioning/API-Lifecycle-Policy)

    `ByokKey` describes a BYOK Key data source.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_confluentcloud as confluentcloud

    azure_key = confluentcloud.get_byok_key(id="cck-abcde")
    pulumi.export("byok", azure_key)
    ```


    :param str id: The ID of the BYOK key, for example, `cck-abcde`.
    """
    ...
