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

__all__ = ['ByokKeyArgs', 'ByokKey']

@pulumi.input_type
class ByokKeyArgs:
    def __init__(__self__, *,
                 aws: Optional[pulumi.Input['ByokKeyAwsArgs']] = None,
                 azure: Optional[pulumi.Input['ByokKeyAzureArgs']] = None,
                 gcp: Optional[pulumi.Input['ByokKeyGcpArgs']] = None):
        """
        The set of arguments for constructing a ByokKey resource.
        :param pulumi.Input['ByokKeyAwsArgs'] aws: (Optional Configuration Block) supports the following:
        :param pulumi.Input['ByokKeyAzureArgs'] azure: (Optional Configuration Block) supports the following:
        :param pulumi.Input['ByokKeyGcpArgs'] gcp: (Optional Configuration Block) supports the following:
        """
        if aws is not None:
            pulumi.set(__self__, "aws", aws)
        if azure is not None:
            pulumi.set(__self__, "azure", azure)
        if gcp is not None:
            pulumi.set(__self__, "gcp", gcp)

    @property
    @pulumi.getter
    def aws(self) -> Optional[pulumi.Input['ByokKeyAwsArgs']]:
        """
        (Optional Configuration Block) supports the following:
        """
        return pulumi.get(self, "aws")

    @aws.setter
    def aws(self, value: Optional[pulumi.Input['ByokKeyAwsArgs']]):
        pulumi.set(self, "aws", value)

    @property
    @pulumi.getter
    def azure(self) -> Optional[pulumi.Input['ByokKeyAzureArgs']]:
        """
        (Optional Configuration Block) supports the following:
        """
        return pulumi.get(self, "azure")

    @azure.setter
    def azure(self, value: Optional[pulumi.Input['ByokKeyAzureArgs']]):
        pulumi.set(self, "azure", value)

    @property
    @pulumi.getter
    def gcp(self) -> Optional[pulumi.Input['ByokKeyGcpArgs']]:
        """
        (Optional Configuration Block) supports the following:
        """
        return pulumi.get(self, "gcp")

    @gcp.setter
    def gcp(self, value: Optional[pulumi.Input['ByokKeyGcpArgs']]):
        pulumi.set(self, "gcp", value)


@pulumi.input_type
class _ByokKeyState:
    def __init__(__self__, *,
                 aws: Optional[pulumi.Input['ByokKeyAwsArgs']] = None,
                 azure: Optional[pulumi.Input['ByokKeyAzureArgs']] = None,
                 gcp: Optional[pulumi.Input['ByokKeyGcpArgs']] = None):
        """
        Input properties used for looking up and filtering ByokKey resources.
        :param pulumi.Input['ByokKeyAwsArgs'] aws: (Optional Configuration Block) supports the following:
        :param pulumi.Input['ByokKeyAzureArgs'] azure: (Optional Configuration Block) supports the following:
        :param pulumi.Input['ByokKeyGcpArgs'] gcp: (Optional Configuration Block) supports the following:
        """
        if aws is not None:
            pulumi.set(__self__, "aws", aws)
        if azure is not None:
            pulumi.set(__self__, "azure", azure)
        if gcp is not None:
            pulumi.set(__self__, "gcp", gcp)

    @property
    @pulumi.getter
    def aws(self) -> Optional[pulumi.Input['ByokKeyAwsArgs']]:
        """
        (Optional Configuration Block) supports the following:
        """
        return pulumi.get(self, "aws")

    @aws.setter
    def aws(self, value: Optional[pulumi.Input['ByokKeyAwsArgs']]):
        pulumi.set(self, "aws", value)

    @property
    @pulumi.getter
    def azure(self) -> Optional[pulumi.Input['ByokKeyAzureArgs']]:
        """
        (Optional Configuration Block) supports the following:
        """
        return pulumi.get(self, "azure")

    @azure.setter
    def azure(self, value: Optional[pulumi.Input['ByokKeyAzureArgs']]):
        pulumi.set(self, "azure", value)

    @property
    @pulumi.getter
    def gcp(self) -> Optional[pulumi.Input['ByokKeyGcpArgs']]:
        """
        (Optional Configuration Block) supports the following:
        """
        return pulumi.get(self, "gcp")

    @gcp.setter
    def gcp(self, value: Optional[pulumi.Input['ByokKeyGcpArgs']]):
        pulumi.set(self, "gcp", value)


class ByokKey(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 aws: Optional[pulumi.Input[pulumi.InputType['ByokKeyAwsArgs']]] = None,
                 azure: Optional[pulumi.Input[pulumi.InputType['ByokKeyAzureArgs']]] = None,
                 gcp: Optional[pulumi.Input[pulumi.InputType['ByokKeyGcpArgs']]] = None,
                 __props__=None):
        """
        [![General Availability](https://img.shields.io/badge/Lifecycle%20Stage-General%20Availability-%2345c6e8)](https://docs.confluent.io/cloud/current/api.html#section/Versioning/API-Lifecycle-Policy)

        `ByokKey` provides a BYOK Key resource that enables creating, editing, and deleting BYOK Key on Confluent Cloud.

        ## Example Usage

        ### Example BYOK Key on Azure

        ```python
        import pulumi
        import pulumi_confluentcloud as confluentcloud

        azure_key = confluentcloud.ByokKey("azure_key", azure=confluentcloud.ByokKeyAzureArgs(
            tenant_id="11111111-1111-1111-1111-111111111111",
            key_vault_id="/subscriptions/11111111-1111-1111-1111-111111111111/resourceGroups/test-vault/providers/Microsoft.KeyVault/vaults/test-vault",
            key_identifier="https://test-vault.vault.azure.net/keys/test-key",
        ))
        ```

        ### Example BYOK Key on GCP

        ```python
        import pulumi
        import pulumi_confluentcloud as confluentcloud

        gcp_key = confluentcloud.ByokKey("gcp_key", gcp=confluentcloud.ByokKeyGcpArgs(
            key_id="projects/temp-gear-123456/locations/us-central1/keyRings/byok-test/cryptoKeys/byok-test",
        ))
        ```

        ## Getting Started

        The following end-to-end examples might help to get started with `ByokKey` resource:
          * dedicated-public-aws-byok-kafka-acls: An example of Encrypting Confluent Cloud Dedicated Kafka Clusters using Self-Managed Keys on AWS.
          * dedicated-public-azure-byok-kafka-acls: An example of Encrypting Confluent Cloud Dedicated Kafka Clusters using Self-Managed Keys on Azure.

        See [Confluent Cloud Bring Your Own Key (BYOK) Management API](https://docs.confluent.io/cloud/current/clusters/byok/index.html) to learn more about Encrypting Confluent Cloud Kafka Clusters using Self-Managed Keys.

        ## Import

        You can import a BYOK Key by using BYOK Key ID. The following example shows how to import a BYOK Key:

        $ export CONFLUENT_CLOUD_API_KEY="<cloud_api_key>"

        $ export CONFLUENT_CLOUD_API_SECRET="<cloud_api_secret>"

        ```sh
        $ pulumi import confluentcloud:index/byokKey:ByokKey aws_key cck-abcde
        ```

        !> **Warning:** Do not forget to delete terminal command history afterwards for security purposes.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[pulumi.InputType['ByokKeyAwsArgs']] aws: (Optional Configuration Block) supports the following:
        :param pulumi.Input[pulumi.InputType['ByokKeyAzureArgs']] azure: (Optional Configuration Block) supports the following:
        :param pulumi.Input[pulumi.InputType['ByokKeyGcpArgs']] gcp: (Optional Configuration Block) supports the following:
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: Optional[ByokKeyArgs] = None,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        [![General Availability](https://img.shields.io/badge/Lifecycle%20Stage-General%20Availability-%2345c6e8)](https://docs.confluent.io/cloud/current/api.html#section/Versioning/API-Lifecycle-Policy)

        `ByokKey` provides a BYOK Key resource that enables creating, editing, and deleting BYOK Key on Confluent Cloud.

        ## Example Usage

        ### Example BYOK Key on Azure

        ```python
        import pulumi
        import pulumi_confluentcloud as confluentcloud

        azure_key = confluentcloud.ByokKey("azure_key", azure=confluentcloud.ByokKeyAzureArgs(
            tenant_id="11111111-1111-1111-1111-111111111111",
            key_vault_id="/subscriptions/11111111-1111-1111-1111-111111111111/resourceGroups/test-vault/providers/Microsoft.KeyVault/vaults/test-vault",
            key_identifier="https://test-vault.vault.azure.net/keys/test-key",
        ))
        ```

        ### Example BYOK Key on GCP

        ```python
        import pulumi
        import pulumi_confluentcloud as confluentcloud

        gcp_key = confluentcloud.ByokKey("gcp_key", gcp=confluentcloud.ByokKeyGcpArgs(
            key_id="projects/temp-gear-123456/locations/us-central1/keyRings/byok-test/cryptoKeys/byok-test",
        ))
        ```

        ## Getting Started

        The following end-to-end examples might help to get started with `ByokKey` resource:
          * dedicated-public-aws-byok-kafka-acls: An example of Encrypting Confluent Cloud Dedicated Kafka Clusters using Self-Managed Keys on AWS.
          * dedicated-public-azure-byok-kafka-acls: An example of Encrypting Confluent Cloud Dedicated Kafka Clusters using Self-Managed Keys on Azure.

        See [Confluent Cloud Bring Your Own Key (BYOK) Management API](https://docs.confluent.io/cloud/current/clusters/byok/index.html) to learn more about Encrypting Confluent Cloud Kafka Clusters using Self-Managed Keys.

        ## Import

        You can import a BYOK Key by using BYOK Key ID. The following example shows how to import a BYOK Key:

        $ export CONFLUENT_CLOUD_API_KEY="<cloud_api_key>"

        $ export CONFLUENT_CLOUD_API_SECRET="<cloud_api_secret>"

        ```sh
        $ pulumi import confluentcloud:index/byokKey:ByokKey aws_key cck-abcde
        ```

        !> **Warning:** Do not forget to delete terminal command history afterwards for security purposes.

        :param str resource_name: The name of the resource.
        :param ByokKeyArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ByokKeyArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 aws: Optional[pulumi.Input[pulumi.InputType['ByokKeyAwsArgs']]] = None,
                 azure: Optional[pulumi.Input[pulumi.InputType['ByokKeyAzureArgs']]] = None,
                 gcp: Optional[pulumi.Input[pulumi.InputType['ByokKeyGcpArgs']]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ByokKeyArgs.__new__(ByokKeyArgs)

            __props__.__dict__["aws"] = aws
            __props__.__dict__["azure"] = azure
            __props__.__dict__["gcp"] = gcp
        super(ByokKey, __self__).__init__(
            'confluentcloud:index/byokKey:ByokKey',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            aws: Optional[pulumi.Input[pulumi.InputType['ByokKeyAwsArgs']]] = None,
            azure: Optional[pulumi.Input[pulumi.InputType['ByokKeyAzureArgs']]] = None,
            gcp: Optional[pulumi.Input[pulumi.InputType['ByokKeyGcpArgs']]] = None) -> 'ByokKey':
        """
        Get an existing ByokKey resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[pulumi.InputType['ByokKeyAwsArgs']] aws: (Optional Configuration Block) supports the following:
        :param pulumi.Input[pulumi.InputType['ByokKeyAzureArgs']] azure: (Optional Configuration Block) supports the following:
        :param pulumi.Input[pulumi.InputType['ByokKeyGcpArgs']] gcp: (Optional Configuration Block) supports the following:
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _ByokKeyState.__new__(_ByokKeyState)

        __props__.__dict__["aws"] = aws
        __props__.__dict__["azure"] = azure
        __props__.__dict__["gcp"] = gcp
        return ByokKey(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def aws(self) -> pulumi.Output['outputs.ByokKeyAws']:
        """
        (Optional Configuration Block) supports the following:
        """
        return pulumi.get(self, "aws")

    @property
    @pulumi.getter
    def azure(self) -> pulumi.Output['outputs.ByokKeyAzure']:
        """
        (Optional Configuration Block) supports the following:
        """
        return pulumi.get(self, "azure")

    @property
    @pulumi.getter
    def gcp(self) -> pulumi.Output['outputs.ByokKeyGcp']:
        """
        (Optional Configuration Block) supports the following:
        """
        return pulumi.get(self, "gcp")

