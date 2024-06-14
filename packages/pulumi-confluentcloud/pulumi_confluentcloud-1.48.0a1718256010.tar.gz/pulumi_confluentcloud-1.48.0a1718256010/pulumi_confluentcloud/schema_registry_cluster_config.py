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

__all__ = ['SchemaRegistryClusterConfigArgs', 'SchemaRegistryClusterConfig']

@pulumi.input_type
class SchemaRegistryClusterConfigArgs:
    def __init__(__self__, *,
                 compatibility_level: Optional[pulumi.Input[str]] = None,
                 credentials: Optional[pulumi.Input['SchemaRegistryClusterConfigCredentialsArgs']] = None,
                 rest_endpoint: Optional[pulumi.Input[str]] = None,
                 schema_registry_cluster: Optional[pulumi.Input['SchemaRegistryClusterConfigSchemaRegistryClusterArgs']] = None):
        """
        The set of arguments for constructing a SchemaRegistryClusterConfig resource.
        :param pulumi.Input[str] compatibility_level: The global Schema Registry compatibility level. Accepted values are: `BACKWARD`, `BACKWARD_TRANSITIVE`, `FORWARD`, `FORWARD_TRANSITIVE`, `FULL`, `FULL_TRANSITIVE`, and `NONE`. See the [Compatibility Types](https://docs.confluent.io/platform/current/schema-registry/avro.html#compatibility-types) for more details.
        :param pulumi.Input['SchemaRegistryClusterConfigCredentialsArgs'] credentials: The Cluster API Credentials.
        :param pulumi.Input[str] rest_endpoint: The REST endpoint of the Schema Registry cluster, for example, `https://psrc-00000.us-central1.gcp.confluent.cloud:443`).
        """
        if compatibility_level is not None:
            pulumi.set(__self__, "compatibility_level", compatibility_level)
        if credentials is not None:
            pulumi.set(__self__, "credentials", credentials)
        if rest_endpoint is not None:
            pulumi.set(__self__, "rest_endpoint", rest_endpoint)
        if schema_registry_cluster is not None:
            pulumi.set(__self__, "schema_registry_cluster", schema_registry_cluster)

    @property
    @pulumi.getter(name="compatibilityLevel")
    def compatibility_level(self) -> Optional[pulumi.Input[str]]:
        """
        The global Schema Registry compatibility level. Accepted values are: `BACKWARD`, `BACKWARD_TRANSITIVE`, `FORWARD`, `FORWARD_TRANSITIVE`, `FULL`, `FULL_TRANSITIVE`, and `NONE`. See the [Compatibility Types](https://docs.confluent.io/platform/current/schema-registry/avro.html#compatibility-types) for more details.
        """
        return pulumi.get(self, "compatibility_level")

    @compatibility_level.setter
    def compatibility_level(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "compatibility_level", value)

    @property
    @pulumi.getter
    def credentials(self) -> Optional[pulumi.Input['SchemaRegistryClusterConfigCredentialsArgs']]:
        """
        The Cluster API Credentials.
        """
        return pulumi.get(self, "credentials")

    @credentials.setter
    def credentials(self, value: Optional[pulumi.Input['SchemaRegistryClusterConfigCredentialsArgs']]):
        pulumi.set(self, "credentials", value)

    @property
    @pulumi.getter(name="restEndpoint")
    def rest_endpoint(self) -> Optional[pulumi.Input[str]]:
        """
        The REST endpoint of the Schema Registry cluster, for example, `https://psrc-00000.us-central1.gcp.confluent.cloud:443`).
        """
        return pulumi.get(self, "rest_endpoint")

    @rest_endpoint.setter
    def rest_endpoint(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "rest_endpoint", value)

    @property
    @pulumi.getter(name="schemaRegistryCluster")
    def schema_registry_cluster(self) -> Optional[pulumi.Input['SchemaRegistryClusterConfigSchemaRegistryClusterArgs']]:
        return pulumi.get(self, "schema_registry_cluster")

    @schema_registry_cluster.setter
    def schema_registry_cluster(self, value: Optional[pulumi.Input['SchemaRegistryClusterConfigSchemaRegistryClusterArgs']]):
        pulumi.set(self, "schema_registry_cluster", value)


@pulumi.input_type
class _SchemaRegistryClusterConfigState:
    def __init__(__self__, *,
                 compatibility_level: Optional[pulumi.Input[str]] = None,
                 credentials: Optional[pulumi.Input['SchemaRegistryClusterConfigCredentialsArgs']] = None,
                 rest_endpoint: Optional[pulumi.Input[str]] = None,
                 schema_registry_cluster: Optional[pulumi.Input['SchemaRegistryClusterConfigSchemaRegistryClusterArgs']] = None):
        """
        Input properties used for looking up and filtering SchemaRegistryClusterConfig resources.
        :param pulumi.Input[str] compatibility_level: The global Schema Registry compatibility level. Accepted values are: `BACKWARD`, `BACKWARD_TRANSITIVE`, `FORWARD`, `FORWARD_TRANSITIVE`, `FULL`, `FULL_TRANSITIVE`, and `NONE`. See the [Compatibility Types](https://docs.confluent.io/platform/current/schema-registry/avro.html#compatibility-types) for more details.
        :param pulumi.Input['SchemaRegistryClusterConfigCredentialsArgs'] credentials: The Cluster API Credentials.
        :param pulumi.Input[str] rest_endpoint: The REST endpoint of the Schema Registry cluster, for example, `https://psrc-00000.us-central1.gcp.confluent.cloud:443`).
        """
        if compatibility_level is not None:
            pulumi.set(__self__, "compatibility_level", compatibility_level)
        if credentials is not None:
            pulumi.set(__self__, "credentials", credentials)
        if rest_endpoint is not None:
            pulumi.set(__self__, "rest_endpoint", rest_endpoint)
        if schema_registry_cluster is not None:
            pulumi.set(__self__, "schema_registry_cluster", schema_registry_cluster)

    @property
    @pulumi.getter(name="compatibilityLevel")
    def compatibility_level(self) -> Optional[pulumi.Input[str]]:
        """
        The global Schema Registry compatibility level. Accepted values are: `BACKWARD`, `BACKWARD_TRANSITIVE`, `FORWARD`, `FORWARD_TRANSITIVE`, `FULL`, `FULL_TRANSITIVE`, and `NONE`. See the [Compatibility Types](https://docs.confluent.io/platform/current/schema-registry/avro.html#compatibility-types) for more details.
        """
        return pulumi.get(self, "compatibility_level")

    @compatibility_level.setter
    def compatibility_level(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "compatibility_level", value)

    @property
    @pulumi.getter
    def credentials(self) -> Optional[pulumi.Input['SchemaRegistryClusterConfigCredentialsArgs']]:
        """
        The Cluster API Credentials.
        """
        return pulumi.get(self, "credentials")

    @credentials.setter
    def credentials(self, value: Optional[pulumi.Input['SchemaRegistryClusterConfigCredentialsArgs']]):
        pulumi.set(self, "credentials", value)

    @property
    @pulumi.getter(name="restEndpoint")
    def rest_endpoint(self) -> Optional[pulumi.Input[str]]:
        """
        The REST endpoint of the Schema Registry cluster, for example, `https://psrc-00000.us-central1.gcp.confluent.cloud:443`).
        """
        return pulumi.get(self, "rest_endpoint")

    @rest_endpoint.setter
    def rest_endpoint(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "rest_endpoint", value)

    @property
    @pulumi.getter(name="schemaRegistryCluster")
    def schema_registry_cluster(self) -> Optional[pulumi.Input['SchemaRegistryClusterConfigSchemaRegistryClusterArgs']]:
        return pulumi.get(self, "schema_registry_cluster")

    @schema_registry_cluster.setter
    def schema_registry_cluster(self, value: Optional[pulumi.Input['SchemaRegistryClusterConfigSchemaRegistryClusterArgs']]):
        pulumi.set(self, "schema_registry_cluster", value)


class SchemaRegistryClusterConfig(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 compatibility_level: Optional[pulumi.Input[str]] = None,
                 credentials: Optional[pulumi.Input[pulumi.InputType['SchemaRegistryClusterConfigCredentialsArgs']]] = None,
                 rest_endpoint: Optional[pulumi.Input[str]] = None,
                 schema_registry_cluster: Optional[pulumi.Input[pulumi.InputType['SchemaRegistryClusterConfigSchemaRegistryClusterArgs']]] = None,
                 __props__=None):
        """
        ## Import

        You can import a Schema Registry Cluster Config by using the Schema Registry cluster ID, Subject name in the format `<Schema Registry cluster ID>`, for example:

        $ export IMPORT_SCHEMA_REGISTRY_API_KEY="<schema_registry_api_key>"

        $ export IMPORT_SCHEMA_REGISTRY_API_SECRET="<schema_registry_api_secret>"

        $ export IMPORT_SCHEMA_REGISTRY_REST_ENDPOINT="<schema_registry_rest_endpoint>"

        ```sh
        $ pulumi import confluentcloud:index/schemaRegistryClusterConfig:SchemaRegistryClusterConfig example lsrc-abc123
        ```

        !> **Warning:** Do not forget to delete terminal command history afterwards for security purposes.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] compatibility_level: The global Schema Registry compatibility level. Accepted values are: `BACKWARD`, `BACKWARD_TRANSITIVE`, `FORWARD`, `FORWARD_TRANSITIVE`, `FULL`, `FULL_TRANSITIVE`, and `NONE`. See the [Compatibility Types](https://docs.confluent.io/platform/current/schema-registry/avro.html#compatibility-types) for more details.
        :param pulumi.Input[pulumi.InputType['SchemaRegistryClusterConfigCredentialsArgs']] credentials: The Cluster API Credentials.
        :param pulumi.Input[str] rest_endpoint: The REST endpoint of the Schema Registry cluster, for example, `https://psrc-00000.us-central1.gcp.confluent.cloud:443`).
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: Optional[SchemaRegistryClusterConfigArgs] = None,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        ## Import

        You can import a Schema Registry Cluster Config by using the Schema Registry cluster ID, Subject name in the format `<Schema Registry cluster ID>`, for example:

        $ export IMPORT_SCHEMA_REGISTRY_API_KEY="<schema_registry_api_key>"

        $ export IMPORT_SCHEMA_REGISTRY_API_SECRET="<schema_registry_api_secret>"

        $ export IMPORT_SCHEMA_REGISTRY_REST_ENDPOINT="<schema_registry_rest_endpoint>"

        ```sh
        $ pulumi import confluentcloud:index/schemaRegistryClusterConfig:SchemaRegistryClusterConfig example lsrc-abc123
        ```

        !> **Warning:** Do not forget to delete terminal command history afterwards for security purposes.

        :param str resource_name: The name of the resource.
        :param SchemaRegistryClusterConfigArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(SchemaRegistryClusterConfigArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 compatibility_level: Optional[pulumi.Input[str]] = None,
                 credentials: Optional[pulumi.Input[pulumi.InputType['SchemaRegistryClusterConfigCredentialsArgs']]] = None,
                 rest_endpoint: Optional[pulumi.Input[str]] = None,
                 schema_registry_cluster: Optional[pulumi.Input[pulumi.InputType['SchemaRegistryClusterConfigSchemaRegistryClusterArgs']]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = SchemaRegistryClusterConfigArgs.__new__(SchemaRegistryClusterConfigArgs)

            __props__.__dict__["compatibility_level"] = compatibility_level
            __props__.__dict__["credentials"] = None if credentials is None else pulumi.Output.secret(credentials)
            __props__.__dict__["rest_endpoint"] = rest_endpoint
            __props__.__dict__["schema_registry_cluster"] = schema_registry_cluster
        secret_opts = pulumi.ResourceOptions(additional_secret_outputs=["credentials"])
        opts = pulumi.ResourceOptions.merge(opts, secret_opts)
        super(SchemaRegistryClusterConfig, __self__).__init__(
            'confluentcloud:index/schemaRegistryClusterConfig:SchemaRegistryClusterConfig',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            compatibility_level: Optional[pulumi.Input[str]] = None,
            credentials: Optional[pulumi.Input[pulumi.InputType['SchemaRegistryClusterConfigCredentialsArgs']]] = None,
            rest_endpoint: Optional[pulumi.Input[str]] = None,
            schema_registry_cluster: Optional[pulumi.Input[pulumi.InputType['SchemaRegistryClusterConfigSchemaRegistryClusterArgs']]] = None) -> 'SchemaRegistryClusterConfig':
        """
        Get an existing SchemaRegistryClusterConfig resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] compatibility_level: The global Schema Registry compatibility level. Accepted values are: `BACKWARD`, `BACKWARD_TRANSITIVE`, `FORWARD`, `FORWARD_TRANSITIVE`, `FULL`, `FULL_TRANSITIVE`, and `NONE`. See the [Compatibility Types](https://docs.confluent.io/platform/current/schema-registry/avro.html#compatibility-types) for more details.
        :param pulumi.Input[pulumi.InputType['SchemaRegistryClusterConfigCredentialsArgs']] credentials: The Cluster API Credentials.
        :param pulumi.Input[str] rest_endpoint: The REST endpoint of the Schema Registry cluster, for example, `https://psrc-00000.us-central1.gcp.confluent.cloud:443`).
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _SchemaRegistryClusterConfigState.__new__(_SchemaRegistryClusterConfigState)

        __props__.__dict__["compatibility_level"] = compatibility_level
        __props__.__dict__["credentials"] = credentials
        __props__.__dict__["rest_endpoint"] = rest_endpoint
        __props__.__dict__["schema_registry_cluster"] = schema_registry_cluster
        return SchemaRegistryClusterConfig(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="compatibilityLevel")
    def compatibility_level(self) -> pulumi.Output[str]:
        """
        The global Schema Registry compatibility level. Accepted values are: `BACKWARD`, `BACKWARD_TRANSITIVE`, `FORWARD`, `FORWARD_TRANSITIVE`, `FULL`, `FULL_TRANSITIVE`, and `NONE`. See the [Compatibility Types](https://docs.confluent.io/platform/current/schema-registry/avro.html#compatibility-types) for more details.
        """
        return pulumi.get(self, "compatibility_level")

    @property
    @pulumi.getter
    def credentials(self) -> pulumi.Output[Optional['outputs.SchemaRegistryClusterConfigCredentials']]:
        """
        The Cluster API Credentials.
        """
        return pulumi.get(self, "credentials")

    @property
    @pulumi.getter(name="restEndpoint")
    def rest_endpoint(self) -> pulumi.Output[Optional[str]]:
        """
        The REST endpoint of the Schema Registry cluster, for example, `https://psrc-00000.us-central1.gcp.confluent.cloud:443`).
        """
        return pulumi.get(self, "rest_endpoint")

    @property
    @pulumi.getter(name="schemaRegistryCluster")
    def schema_registry_cluster(self) -> pulumi.Output[Optional['outputs.SchemaRegistryClusterConfigSchemaRegistryCluster']]:
        return pulumi.get(self, "schema_registry_cluster")

