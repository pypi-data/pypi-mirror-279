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

__all__ = ['KafkaClusterConfigArgs', 'KafkaClusterConfig']

@pulumi.input_type
class KafkaClusterConfigArgs:
    def __init__(__self__, *,
                 config: pulumi.Input[Mapping[str, pulumi.Input[str]]],
                 credentials: Optional[pulumi.Input['KafkaClusterConfigCredentialsArgs']] = None,
                 kafka_cluster: Optional[pulumi.Input['KafkaClusterConfigKafkaClusterArgs']] = None,
                 rest_endpoint: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a KafkaClusterConfig resource.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] config: The custom cluster settings to set:
        :param pulumi.Input['KafkaClusterConfigCredentialsArgs'] credentials: The Cluster API Credentials.
        :param pulumi.Input[str] rest_endpoint: The REST endpoint of the Dedicated Kafka cluster, for example, `https://pkc-00000.us-central1.gcp.confluent.cloud:443`).
        """
        pulumi.set(__self__, "config", config)
        if credentials is not None:
            pulumi.set(__self__, "credentials", credentials)
        if kafka_cluster is not None:
            pulumi.set(__self__, "kafka_cluster", kafka_cluster)
        if rest_endpoint is not None:
            pulumi.set(__self__, "rest_endpoint", rest_endpoint)

    @property
    @pulumi.getter
    def config(self) -> pulumi.Input[Mapping[str, pulumi.Input[str]]]:
        """
        The custom cluster settings to set:
        """
        return pulumi.get(self, "config")

    @config.setter
    def config(self, value: pulumi.Input[Mapping[str, pulumi.Input[str]]]):
        pulumi.set(self, "config", value)

    @property
    @pulumi.getter
    def credentials(self) -> Optional[pulumi.Input['KafkaClusterConfigCredentialsArgs']]:
        """
        The Cluster API Credentials.
        """
        return pulumi.get(self, "credentials")

    @credentials.setter
    def credentials(self, value: Optional[pulumi.Input['KafkaClusterConfigCredentialsArgs']]):
        pulumi.set(self, "credentials", value)

    @property
    @pulumi.getter(name="kafkaCluster")
    def kafka_cluster(self) -> Optional[pulumi.Input['KafkaClusterConfigKafkaClusterArgs']]:
        return pulumi.get(self, "kafka_cluster")

    @kafka_cluster.setter
    def kafka_cluster(self, value: Optional[pulumi.Input['KafkaClusterConfigKafkaClusterArgs']]):
        pulumi.set(self, "kafka_cluster", value)

    @property
    @pulumi.getter(name="restEndpoint")
    def rest_endpoint(self) -> Optional[pulumi.Input[str]]:
        """
        The REST endpoint of the Dedicated Kafka cluster, for example, `https://pkc-00000.us-central1.gcp.confluent.cloud:443`).
        """
        return pulumi.get(self, "rest_endpoint")

    @rest_endpoint.setter
    def rest_endpoint(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "rest_endpoint", value)


@pulumi.input_type
class _KafkaClusterConfigState:
    def __init__(__self__, *,
                 config: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 credentials: Optional[pulumi.Input['KafkaClusterConfigCredentialsArgs']] = None,
                 kafka_cluster: Optional[pulumi.Input['KafkaClusterConfigKafkaClusterArgs']] = None,
                 rest_endpoint: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering KafkaClusterConfig resources.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] config: The custom cluster settings to set:
        :param pulumi.Input['KafkaClusterConfigCredentialsArgs'] credentials: The Cluster API Credentials.
        :param pulumi.Input[str] rest_endpoint: The REST endpoint of the Dedicated Kafka cluster, for example, `https://pkc-00000.us-central1.gcp.confluent.cloud:443`).
        """
        if config is not None:
            pulumi.set(__self__, "config", config)
        if credentials is not None:
            pulumi.set(__self__, "credentials", credentials)
        if kafka_cluster is not None:
            pulumi.set(__self__, "kafka_cluster", kafka_cluster)
        if rest_endpoint is not None:
            pulumi.set(__self__, "rest_endpoint", rest_endpoint)

    @property
    @pulumi.getter
    def config(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        The custom cluster settings to set:
        """
        return pulumi.get(self, "config")

    @config.setter
    def config(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "config", value)

    @property
    @pulumi.getter
    def credentials(self) -> Optional[pulumi.Input['KafkaClusterConfigCredentialsArgs']]:
        """
        The Cluster API Credentials.
        """
        return pulumi.get(self, "credentials")

    @credentials.setter
    def credentials(self, value: Optional[pulumi.Input['KafkaClusterConfigCredentialsArgs']]):
        pulumi.set(self, "credentials", value)

    @property
    @pulumi.getter(name="kafkaCluster")
    def kafka_cluster(self) -> Optional[pulumi.Input['KafkaClusterConfigKafkaClusterArgs']]:
        return pulumi.get(self, "kafka_cluster")

    @kafka_cluster.setter
    def kafka_cluster(self, value: Optional[pulumi.Input['KafkaClusterConfigKafkaClusterArgs']]):
        pulumi.set(self, "kafka_cluster", value)

    @property
    @pulumi.getter(name="restEndpoint")
    def rest_endpoint(self) -> Optional[pulumi.Input[str]]:
        """
        The REST endpoint of the Dedicated Kafka cluster, for example, `https://pkc-00000.us-central1.gcp.confluent.cloud:443`).
        """
        return pulumi.get(self, "rest_endpoint")

    @rest_endpoint.setter
    def rest_endpoint(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "rest_endpoint", value)


class KafkaClusterConfig(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 config: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 credentials: Optional[pulumi.Input[pulumi.InputType['KafkaClusterConfigCredentialsArgs']]] = None,
                 kafka_cluster: Optional[pulumi.Input[pulumi.InputType['KafkaClusterConfigKafkaClusterArgs']]] = None,
                 rest_endpoint: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        ## Import

        You can import a Kafka cluster config by using the Kafka cluster ID, for example:

        Option #1: Manage multiple Kafka clusters in the same Terraform workspace

        $ export IMPORT_KAFKA_API_KEY="<kafka_api_key>"

        $ export IMPORT_KAFKA_API_SECRET="<kafka_api_secret>"

        $ export IMPORT_KAFKA_REST_ENDPOINT="<kafka_rest_endpoint>"

        ```sh
        $ pulumi import confluentcloud:index/kafkaClusterConfig:KafkaClusterConfig test lkc-abc123
        ```

        Option #2: Manage a single Kafka cluster in the same Terraform workspace

        ```sh
        $ pulumi import confluentcloud:index/kafkaClusterConfig:KafkaClusterConfig test lkc-abc123
        ```

        !> **Warning:** Do not forget to delete terminal command history afterwards for security purposes.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] config: The custom cluster settings to set:
        :param pulumi.Input[pulumi.InputType['KafkaClusterConfigCredentialsArgs']] credentials: The Cluster API Credentials.
        :param pulumi.Input[str] rest_endpoint: The REST endpoint of the Dedicated Kafka cluster, for example, `https://pkc-00000.us-central1.gcp.confluent.cloud:443`).
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: KafkaClusterConfigArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        ## Import

        You can import a Kafka cluster config by using the Kafka cluster ID, for example:

        Option #1: Manage multiple Kafka clusters in the same Terraform workspace

        $ export IMPORT_KAFKA_API_KEY="<kafka_api_key>"

        $ export IMPORT_KAFKA_API_SECRET="<kafka_api_secret>"

        $ export IMPORT_KAFKA_REST_ENDPOINT="<kafka_rest_endpoint>"

        ```sh
        $ pulumi import confluentcloud:index/kafkaClusterConfig:KafkaClusterConfig test lkc-abc123
        ```

        Option #2: Manage a single Kafka cluster in the same Terraform workspace

        ```sh
        $ pulumi import confluentcloud:index/kafkaClusterConfig:KafkaClusterConfig test lkc-abc123
        ```

        !> **Warning:** Do not forget to delete terminal command history afterwards for security purposes.

        :param str resource_name: The name of the resource.
        :param KafkaClusterConfigArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(KafkaClusterConfigArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 config: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 credentials: Optional[pulumi.Input[pulumi.InputType['KafkaClusterConfigCredentialsArgs']]] = None,
                 kafka_cluster: Optional[pulumi.Input[pulumi.InputType['KafkaClusterConfigKafkaClusterArgs']]] = None,
                 rest_endpoint: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = KafkaClusterConfigArgs.__new__(KafkaClusterConfigArgs)

            if config is None and not opts.urn:
                raise TypeError("Missing required property 'config'")
            __props__.__dict__["config"] = config
            __props__.__dict__["credentials"] = None if credentials is None else pulumi.Output.secret(credentials)
            __props__.__dict__["kafka_cluster"] = kafka_cluster
            __props__.__dict__["rest_endpoint"] = rest_endpoint
        secret_opts = pulumi.ResourceOptions(additional_secret_outputs=["credentials"])
        opts = pulumi.ResourceOptions.merge(opts, secret_opts)
        super(KafkaClusterConfig, __self__).__init__(
            'confluentcloud:index/kafkaClusterConfig:KafkaClusterConfig',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            config: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            credentials: Optional[pulumi.Input[pulumi.InputType['KafkaClusterConfigCredentialsArgs']]] = None,
            kafka_cluster: Optional[pulumi.Input[pulumi.InputType['KafkaClusterConfigKafkaClusterArgs']]] = None,
            rest_endpoint: Optional[pulumi.Input[str]] = None) -> 'KafkaClusterConfig':
        """
        Get an existing KafkaClusterConfig resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] config: The custom cluster settings to set:
        :param pulumi.Input[pulumi.InputType['KafkaClusterConfigCredentialsArgs']] credentials: The Cluster API Credentials.
        :param pulumi.Input[str] rest_endpoint: The REST endpoint of the Dedicated Kafka cluster, for example, `https://pkc-00000.us-central1.gcp.confluent.cloud:443`).
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _KafkaClusterConfigState.__new__(_KafkaClusterConfigState)

        __props__.__dict__["config"] = config
        __props__.__dict__["credentials"] = credentials
        __props__.__dict__["kafka_cluster"] = kafka_cluster
        __props__.__dict__["rest_endpoint"] = rest_endpoint
        return KafkaClusterConfig(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def config(self) -> pulumi.Output[Mapping[str, str]]:
        """
        The custom cluster settings to set:
        """
        return pulumi.get(self, "config")

    @property
    @pulumi.getter
    def credentials(self) -> pulumi.Output[Optional['outputs.KafkaClusterConfigCredentials']]:
        """
        The Cluster API Credentials.
        """
        return pulumi.get(self, "credentials")

    @property
    @pulumi.getter(name="kafkaCluster")
    def kafka_cluster(self) -> pulumi.Output[Optional['outputs.KafkaClusterConfigKafkaCluster']]:
        return pulumi.get(self, "kafka_cluster")

    @property
    @pulumi.getter(name="restEndpoint")
    def rest_endpoint(self) -> pulumi.Output[Optional[str]]:
        """
        The REST endpoint of the Dedicated Kafka cluster, for example, `https://pkc-00000.us-central1.gcp.confluent.cloud:443`).
        """
        return pulumi.get(self, "rest_endpoint")

