# -*- coding: utf-8 -*-

"""
Abstract dataclass for RDS DB instance, cluster.
"""

import typing as T
import sys
import enum
import time
import dataclasses
from datetime import datetime

from iterproxy import IterProxy
from func_args import resolve_kwargs, NOTHING

from .vendor.waiter import Waiter
from .exc import StatusError

if T.TYPE_CHECKING:  # pragma: no cover
    from mypy_boto3_rds.client import RDSClient


class RDSDBInstanceStatusEnum(str, enum.Enum):
    """
    RDS DB instance status enum. The official document doesn't mention the exact
    string. But I found it is all lower case slugified.

    Reference:

    - https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/accessing-monitoring.html#Overview.DBInstance.Status
    """

    # fmt: off
    available = "available"
    backing_up = "backing-up"
    configuring_enhanced_monitoring = "configuring-enhanced-monitoring"
    configuring_iam_database_auth = "configuring-iam-database-auth"
    configuring_log_exports = "configuring-log-exports"
    converting_to_vpc = "converting-to-vpc"
    creating = "creating"
    delete_precheck = "delete-precheck"
    deleting = "deleting"
    failed = "failed"
    inaccessible_encryption_credentials = "inaccessible-encryption-credentials"
    inaccessible_encryption_credentials_recoverable ="inaccessible-encryption-credentials-recoverable"
    incompatible_network = "incompatible-network"
    incompatible_option_group = "incompatible-option-group"
    incompatible_parameters = "incompatible-parameters"
    incompatible_restore = "incompatible-restore"
    insufficient_capacity = "insufficient-capacity"
    maintenance = "maintenance"
    modifying = "modifying"
    moving_to_vpc = "moving-to-vpc"
    rebooting = "rebooting"
    resetting_master_credentials = "resetting-master-credentials"
    renaming = "renaming"
    restore_error = "restore-error"
    starting = "starting"
    stopped = "stopped"
    stopping = "stopping"
    storage_full = "storage-full"
    storage_optimization = "storage-optimization"
    upgrading = "upgrading"
    # fmt: on


T_STATUS_ENUM_SET = T.Set[RDSDBInstanceStatusEnum]


class RDSDBInstanceStatusGroupEnum:
    """
    Group RDS DB instance status enum by semantic.

    :param ended: The status that the instance can be considered as "stopped", "won't change".
    :param in_transition: The status that the instance can be considered as "changing".
    :param impossible_to_become_available: as the name
    :param impossible_to_become_stopped: as the name
    """

    ended: T_STATUS_ENUM_SET = {
        RDSDBInstanceStatusEnum.available,
        RDSDBInstanceStatusEnum.failed,
        RDSDBInstanceStatusEnum.stopped,
        RDSDBInstanceStatusEnum.inaccessible_encryption_credentials,
        RDSDBInstanceStatusEnum.inaccessible_encryption_credentials_recoverable,
        RDSDBInstanceStatusEnum.incompatible_network,
        RDSDBInstanceStatusEnum.incompatible_option_group,
        RDSDBInstanceStatusEnum.incompatible_parameters,
        RDSDBInstanceStatusEnum.incompatible_restore,
        RDSDBInstanceStatusEnum.insufficient_capacity,
        RDSDBInstanceStatusEnum.restore_error,
    }

    in_transition: T_STATUS_ENUM_SET = {
        RDSDBInstanceStatusEnum.backing_up,
        RDSDBInstanceStatusEnum.configuring_enhanced_monitoring,
        RDSDBInstanceStatusEnum.configuring_iam_database_auth,
        RDSDBInstanceStatusEnum.configuring_log_exports,
        RDSDBInstanceStatusEnum.converting_to_vpc,
        RDSDBInstanceStatusEnum.creating,
        RDSDBInstanceStatusEnum.deleting,
        RDSDBInstanceStatusEnum.maintenance,
        RDSDBInstanceStatusEnum.modifying,
        RDSDBInstanceStatusEnum.moving_to_vpc,
        RDSDBInstanceStatusEnum.rebooting,
        RDSDBInstanceStatusEnum.resetting_master_credentials,
        RDSDBInstanceStatusEnum.renaming,
        RDSDBInstanceStatusEnum.starting,
        RDSDBInstanceStatusEnum.stopping,
        RDSDBInstanceStatusEnum.storage_optimization,
        RDSDBInstanceStatusEnum.upgrading,
    }

    impossible_to_become_available: T_STATUS_ENUM_SET = (
        {
            RDSDBInstanceStatusEnum.deleting,
            RDSDBInstanceStatusEnum.stopping,
        }
        .union(ended)
        .difference(
            {
                RDSDBInstanceStatusEnum.available,
            }
        )
    )

    impossible_to_become_stopped: T_STATUS_ENUM_SET = in_transition.union(
        ended
    ).difference(
        {
            RDSDBInstanceStatusEnum.stopping,
            RDSDBInstanceStatusEnum.stopped,
        }
    )


@dataclasses.dataclass
class RDSDBInstance:
    """
    Represent an RDS DB instance.

    See attributes explanation at:
    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb/client/describe_db_instances.html
    """

    # fmt: off
    id: str = dataclasses.field()
    status: str = dataclasses.field()
    instance_class: T.Optional[str] = dataclasses.field(default=None)
    instance_create_time: T.Optional[datetime] = dataclasses.field(default=None)
    engine: T.Optional[str] = dataclasses.field(default=None)
    engine_version: T.Optional[str] = dataclasses.field(default=None)
    endpoint: T.Optional[str] = dataclasses.field(default=None)
    port: T.Optional[int] = dataclasses.field(default=None)
    hosted_zone_id: T.Optional[str] = dataclasses.field(default=None)
    master_username: T.Optional[str] = dataclasses.field(default=None)
    allocated_storage: T.Optional[str] = dataclasses.field(default=None)
    preferred_backup_window: T.Optional[str] = dataclasses.field(default=None)
    backup_retention_period: T.Optional[int] = dataclasses.field(default=None)
    preferred_maintenance_window: T.Optional[str] = dataclasses.field(default=None)
    latest_restorable_time: T.Optional[datetime] = dataclasses.field(default=None)
    multi_az: T.Optional[bool] = dataclasses.field(default=None)
    auto_minor_version_upgrade: T.Optional[bool] = dataclasses.field(default=None)
    replica_mode: T.Optional[str] = dataclasses.field(default=None)
    license_model: T.Optional[str] = dataclasses.field(default=None)
    iops: T.Optional[int] = dataclasses.field(default=None)
    character_set_name: T.Optional[str] = dataclasses.field(default=None)
    secondary_availability_zone: T.Optional[str] = dataclasses.field(default=None)
    publicly_accessible: T.Optional[bool] = dataclasses.field(default=None)
    storage_type: T.Optional[str] = dataclasses.field(default=None)
    tde_credential_arn: T.Optional[str] = dataclasses.field(default=None)
    db_instance_port: T.Optional[int] = dataclasses.field(default=None)
    db_cluster_identifier: T.Optional[str] = dataclasses.field(default=None)
    storage_encrypted: T.Optional[bool] = dataclasses.field(default=None)
    kms_key_id: T.Optional[str] = dataclasses.field(default=None)
    dbi_resource_id: T.Optional[str] = dataclasses.field(default=None)
    ca_certificate_identifier: T.Optional[str] = dataclasses.field(default=None)
    copy_tags_to_snapshot: T.Optional[bool] = dataclasses.field(default=None)
    monitoring_interval: T.Optional[int] = dataclasses.field(default=None)
    enhanced_monitoring_resource_arn: T.Optional[str] = dataclasses.field(default=None)
    monitoring_role_arn: T.Optional[str] = dataclasses.field(default=None)
    promotion_tier: T.Optional[int] = dataclasses.field(default=None)
    db_instance_arn: T.Optional[str] = dataclasses.field(default=None)
    timezone: T.Optional[str] = dataclasses.field(default=None)
    iam_database_authentication_enabled: T.Optional[bool] = dataclasses.field(default=None)
    performance_insights_enabled: T.Optional[bool] = dataclasses.field(default=None)
    performance_insights_kms_key_id: T.Optional[str] = dataclasses.field(default=None)
    performance_insights_retention_period: T.Optional[int] = dataclasses.field(default=None)
    deletion_protection: T.Optional[bool] = dataclasses.field(default=None)
    max_allocated_storage: T.Optional[int] = dataclasses.field(default=None)
    customer_owned_ip_enabled: T.Optional[bool] = dataclasses.field(default=None)
    aws_backup_recovery_point_arn: T.Optional[str] = dataclasses.field(default=None)
    activity_stream_status: T.Optional[str] = dataclasses.field(default=None)
    activity_stream_kms_key_id: T.Optional[str] = dataclasses.field(default=None)
    activity_stream_kinesis_stream_name: T.Optional[str] = dataclasses.field(default=None)
    activity_stream_mode: T.Optional[str] = dataclasses.field(default=None)
    activity_stream_engine_native_audit_fields_included: T.Optional[bool] = dataclasses.field(default=None)
    automation_mode: T.Optional[str] = dataclasses.field(default=None)
    resume_full_automation_mode_time: T.Optional[datetime] = dataclasses.field(default=None)
    custom_iam_instance_profile: T.Optional[str] = dataclasses.field(default=None)
    backup_target: T.Optional[str] = dataclasses.field(default=None)
    network_type: T.Optional[str] = dataclasses.field(default=None)
    activity_stream_policy_status: T.Optional[str] = dataclasses.field(default=None)
    storage_throughput: T.Optional[int] = dataclasses.field(default=None)
    db_system_id: T.Optional[str] = dataclasses.field(default=None)
    read_replica_source_db_cluster_identifier: T.Optional[str] = dataclasses.field(default=None)
    vpc_id: T.Optional[str] = dataclasses.field(default=None)
    subnet_ids: T.List[str] = dataclasses.field(default_factory=list)
    subnet_group_name: T.Optional[str] = dataclasses.field(default=None)
    subnet_group_description: T.Optional[str] = dataclasses.field(default=None)
    subnet_group_arn: T.Optional[str] = dataclasses.field(default=None)
    subnet_group_status: T.Optional[str] = dataclasses.field(default=None)
    security_groups: T.List[T.Dict[str, str]] = dataclasses.field(default_factory=list)
    availability_zone: T.Optional[str] = dataclasses.field(default=None)
    tags: T.Dict[str, str] = dataclasses.field(default_factory=dict)
    data: T.Dict[str, T.Any] = dataclasses.field(default_factory=dict)
    # fmt: on

    @classmethod
    def from_dict(cls, dct: dict):
        """
        Create an RDS DB instance object from the ``describe_db_instances`` API response.
        """
        # fmt: off
        return cls(
            id=dct["DBInstanceIdentifier"],
            status=dct["DBInstanceStatus"],
            instance_class=dct.get("DBInstanceClass"),
            instance_create_time=dct.get("InstanceCreateTime"),
            engine=dct.get("Engine"),
            engine_version=dct.get("EngineVersion"),
            endpoint=dct.get("Endpoint", {}).get("Address"),
            port=dct.get("Endpoint", {}).get("Port"),
            hosted_zone_id=dct.get("Endpoint", {}).get("HostedZoneId"),
            master_username=dct.get("MasterUsername"),
            allocated_storage=dct.get("AllocatedStorage"),
            preferred_backup_window=dct.get("PreferredBackupWindow"),
            backup_retention_period=dct.get("BackupRetentionPeriod"),
            preferred_maintenance_window=dct.get("PreferredMaintenanceWindow"),
            latest_restorable_time=dct.get("LatestRestorableTime"),
            multi_az=dct.get("MultiAZ"),
            auto_minor_version_upgrade=dct.get("AutoMinorVersionUpgrade"),
            replica_mode=dct.get("ReplicaMode"),
            license_model=dct.get("LicenseModel"),
            iops=dct.get("Iops"),
            character_set_name=dct.get("CharacterSetName"),
            secondary_availability_zone=dct.get("SecondaryAvailabilityZone"),
            publicly_accessible=dct.get("PubliclyAccessible"),
            storage_type=dct.get("StorageType"),
            tde_credential_arn=dct.get("TdeCredentialArn"),
            db_instance_port=dct.get("DbInstancePort"),
            db_cluster_identifier=dct.get("DBClusterIdentifier"),
            storage_encrypted=dct.get("StorageEncrypted"),
            kms_key_id=dct.get("KmsKeyId"),
            dbi_resource_id=dct.get("DbiResourceId"),
            ca_certificate_identifier=dct.get("CACertificateIdentifier"),
            copy_tags_to_snapshot=dct.get("CopyTagsToSnapshot"),
            monitoring_interval=dct.get("MonitoringInterval"),
            enhanced_monitoring_resource_arn=dct.get("EnhancedMonitoringResourceArn"),
            monitoring_role_arn=dct.get("MonitoringRoleArn"),
            promotion_tier=dct.get("PromotionTier"),
            db_instance_arn=dct.get("DBInstanceArn"),
            timezone=dct.get("Timezone"),
            iam_database_authentication_enabled=dct.get("IAMDatabaseAuthenticationEnabled"),
            performance_insights_enabled=dct.get("PerformanceInsightsEnabled"),
            performance_insights_kms_key_id=dct.get("PerformanceInsightsKMSKeyId"),
            performance_insights_retention_period=dct.get("PerformanceInsightsRetentionPeriod"),
            deletion_protection=dct.get("DeletionProtection"),
            max_allocated_storage=dct.get("MaxAllocatedStorage"),
            customer_owned_ip_enabled=dct.get("CustomerOwnedIpEnabled"),
            aws_backup_recovery_point_arn=dct.get("AwsBackupRecoveryPointArn"),
            activity_stream_status=dct.get("ActivityStreamStatus"),
            activity_stream_kms_key_id=dct.get("ActivityStreamKmsKeyId"),
            activity_stream_kinesis_stream_name=dct.get("ActivityStreamKinesisStreamName"),
            activity_stream_mode=dct.get("ActivityStreamMode"),
            activity_stream_engine_native_audit_fields_included=dct.get("ActivityStreamEngineNativeAuditFieldsIncluded"),
            automation_mode=dct.get("AutomationMode"),
            resume_full_automation_mode_time=dct.get("ResumeFullAutomationModeTime"),
            custom_iam_instance_profile=dct.get("CustomIamInstanceProfile"),
            backup_target=dct.get("BackupTarget"),
            network_type=dct.get("NetworkType"),
            activity_stream_policy_status=dct.get("ActivityStreamPolicyStatus"),
            storage_throughput=dct.get("StorageThroughput"),
            db_system_id=dct.get("DBSystemId"),
            read_replica_source_db_cluster_identifier=dct.get("ReadReplicaSourceDBClusterIdentifier"),
            vpc_id=dct.get("DBSubnetGroup", {}).get("VpcId"),
            subnet_ids=[
                kv["SubnetIdentifier"]
                for kv in dct.get("DBSubnetGroup", {}).get("Subnets", [])
            ],
            subnet_group_name=dct.get("DBSubnetGroup", {}).get("DBSubnetGroupName"),
            subnet_group_description=dct.get("DBSubnetGroup", {}).get("DBSubnetGroupDescription"),
            subnet_group_arn=dct.get("DBSubnetGroup", {}).get("DBSubnetGroupArn"),
            subnet_group_status=dct.get("DBSubnetGroup", {}).get("SubnetGroupStatus"),
            security_groups=dct.get("DBSecurityGroups", []),
            availability_zone=dct.get("AvailabilityZone"),
            tags={d["Key"]: d["Value"] for d in dct.get("TagList", [])},
            data=dct,
        )
        # fmt: on

    # status checking methods human intuitive status check
    def is_available(self) -> bool:  # pragma: no cover
        """ """
        return self.status == RDSDBInstanceStatusEnum.available.value

    def is_backing_up(self) -> bool:  # pragma: no cover
        """ """
        return self.status == RDSDBInstanceStatusEnum.backing_up.value

    def is_configuring_enhanced_monitoring(self) -> bool:  # pragma: no cover
        """ """
        return (
            self.status == RDSDBInstanceStatusEnum.configuring_enhanced_monitoring.value
        )

    def is_configuring_iam_database_auth(self) -> bool:  # pragma: no cover
        """ """
        return (
            self.status == RDSDBInstanceStatusEnum.configuring_iam_database_auth.value
        )

    def is_configuring_log_exports(self) -> bool:  # pragma: no cover
        """ """
        return self.status == RDSDBInstanceStatusEnum.configuring_log_exports.value

    def is_converting_to_vpc(self) -> bool:  # pragma: no cover
        """ """
        return self.status == RDSDBInstanceStatusEnum.converting_to_vpc.value

    def is_creating(self) -> bool:  # pragma: no cover
        """ """
        return self.status == RDSDBInstanceStatusEnum.creating.value

    def is_delete_precheck(self) -> bool:  # pragma: no cover
        """ """
        return self.status == RDSDBInstanceStatusEnum.delete_precheck.value

    def is_deleting(self) -> bool:  # pragma: no cover
        """ """
        return self.status == RDSDBInstanceStatusEnum.deleting.value

    def is_failed(self) -> bool:  # pragma: no cover
        """ """
        return self.status == RDSDBInstanceStatusEnum.failed.value

    def is_inaccessible_encryption_credentials(self) -> bool:  # pragma: no cover
        """ """
        return (
            self.status
            == RDSDBInstanceStatusEnum.inaccessible_encryption_credentials.value
        )

    def is_inaccessible_encryption_credentials_recoverable(
        self,
    ) -> bool:  # pragma: no cover
        """ """
        return (
            self.status
            == RDSDBInstanceStatusEnum.inaccessible_encryption_credentials_recoverable.value
        )

    def is_incompatible_network(self) -> bool:  # pragma: no cover
        """ """
        return self.status == RDSDBInstanceStatusEnum.incompatible_network.value

    def is_incompatible_option_group(self) -> bool:  # pragma: no cover
        """ """
        return self.status == RDSDBInstanceStatusEnum.incompatible_option_group.value

    def is_incompatible_parameters(self) -> bool:  # pragma: no cover
        """ """
        return self.status == RDSDBInstanceStatusEnum.incompatible_parameters.value

    def is_incompatible_restore(self) -> bool:  # pragma: no cover
        """ """
        return self.status == RDSDBInstanceStatusEnum.incompatible_restore.value

    def is_insufficient_capacity(self) -> bool:  # pragma: no cover
        """ """
        return self.status == RDSDBInstanceStatusEnum.insufficient_capacity.value

    def is_maintenance(self) -> bool:  # pragma: no cover
        """ """
        return self.status == RDSDBInstanceStatusEnum.maintenance.value

    def is_modifying(self) -> bool:  # pragma: no cover
        """ """
        return self.status == RDSDBInstanceStatusEnum.modifying.value

    def is_moving_to_vpc(self) -> bool:  # pragma: no cover
        """ """
        return self.status == RDSDBInstanceStatusEnum.moving_to_vpc.value

    def is_rebooting(self) -> bool:  # pragma: no cover
        """ """
        return self.status == RDSDBInstanceStatusEnum.rebooting.value

    def is_resetting_master_credentials(self) -> bool:  # pragma: no cover
        """ """
        return self.status == RDSDBInstanceStatusEnum.resetting_master_credentials.value

    def is_renaming(self) -> bool:  # pragma: no cover
        """ """
        return self.status == RDSDBInstanceStatusEnum.renaming.value

    def is_restore_error(self) -> bool:  # pragma: no cover
        """ """
        return self.status == RDSDBInstanceStatusEnum.restore_error.value

    def is_starting(self) -> bool:  # pragma: no cover
        """ """
        return self.status == RDSDBInstanceStatusEnum.starting.value

    def is_stopped(self) -> bool:  # pragma: no cover
        """ """
        return self.status == RDSDBInstanceStatusEnum.stopped.value

    def is_stopping(self) -> bool:  # pragma: no cover
        """ """
        return self.status == RDSDBInstanceStatusEnum.stopping.value

    def is_storage_full(self) -> bool:  # pragma: no cover
        """ """
        return self.status == RDSDBInstanceStatusEnum.storage_full.value

    def is_storage_optimization(self) -> bool:  # pragma: no cover
        """ """
        return self.status == RDSDBInstanceStatusEnum.storage_optimization.value

    def is_upgrading(self) -> bool:  # pragma: no cover
        """ """
        return self.status == RDSDBInstanceStatusEnum.upgrading.value

    # more human intuitive status check
    def is_ready_to_start(self) -> bool:
        """ """
        return self.is_stopped()

    def is_ready_to_stop(self) -> bool:
        """ """
        return self.is_available()

    def is_end(self) -> bool:
        """ """
        return self.status in {
            status.value for status in RDSDBInstanceStatusGroupEnum.ended
        }

    def is_in_transition(self) -> bool:
        """ """
        return self.status in {
            status.value for status in RDSDBInstanceStatusGroupEnum.in_transition
        }

    def start_db_instance(self, rds_client: "RDSClient") -> dict:
        """
        Start the RDS DB instance
        """
        return rds_client.start_db_instance(DBInstanceIdentifier=self.id)

    def stop_db_instance(self, rds_client: "RDSClient") -> dict:
        """
        Stop the RDS DB instance
        """
        return rds_client.stop_db_instance(DBInstanceIdentifier=self.id)

    def delete_db_instance(
        self,
        rds_client: "RDSClient",
        skip_final_snapshot: bool = NOTHING,
        final_db_snapshot_identifier: str = NOTHING,
        delete_automated_backups: bool = NOTHING,
    ) -> dict:
        """
        Delete the RDS DB instance
        """
        return rds_client.delete_db_instance(
            **resolve_kwargs(
                DBInstanceIdentifier=self.id,
                SkipFinalSnapshot=skip_final_snapshot,
                FinalDBSnapshotIdentifier=final_db_snapshot_identifier,
                DeleteAutomatedBackups=delete_automated_backups,
            )
        )

    def wait_for_status(
        self,
        rds_client: "RDSClient",
        stop_status: T.Union[RDSDBInstanceStatusEnum, T.List[RDSDBInstanceStatusEnum]],
        gap: T.Union[int, float] = 1,
        delays: T.Union[int, float] = 10,
        timeout: T.Union[int, float] = 300,
        instant: bool = True,
        error_status: T.Optional[
            T.Union[RDSDBInstanceStatusEnum, T.List[RDSDBInstanceStatusEnum]]
        ] = None,
        indent: int = 0,
        verbose: bool = True,
    ) -> "RDSDBInstance":  # pragma: no cover
        """
        wait until the DB instance reaches the specified status defined in
        ``stop_status``. If reaches any of ``error_status ``, raise error.

        :param rds_client:
        :param stop_status: status to stop waiting
        :param gap: the time to wait before making first status check
        :param delays: delay between each check
        :param timeout: timeout in seconds
        :param instant: if True, then the first check is instant
        :param error_status: status to raise error
        :param indent: indent level for logging
        :param verbose: whether to print log

        :return: the :class:`RDSDBInstance` representing the latest status
            of DB instance.
        """
        if isinstance(stop_status, RDSDBInstanceStatusEnum):
            stop_status_set = {stop_status.value}
        else:
            stop_status_set = {status.value for status in RDSDBInstanceStatusEnum}
        if error_status is None:
            error_status_set = set()
        elif isinstance(error_status, RDSDBInstanceStatusEnum):
            error_status_set = {error_status.value}
        else:
            error_status_set = {status.value for status in RDSDBInstanceStatusEnum}

        for attempt, elapse in Waiter(
            delays=delays,
            timeout=timeout,
            instant=instant,
            indent=indent,
            verbose=verbose,
        ):
            db_inst = self.from_id(rds_client, self.id)
            if db_inst.status in stop_status_set:
                sys.stdout.write("\n")
                return db_inst
            elif db_inst.status in error_status_set:
                raise StatusError(f"stop because status reaches {db_inst.status!r}")
            else:
                pass

    def wait_for_available(
        self,
        rds_client: "RDSClient",
        delays: T.Union[int, float] = 10,
        timeout: T.Union[int, float] = 300,
        indent: int = 0,
        verbose: bool = True,
    ) -> "RDSDBInstance":  # pragma: no cover
        """
        Similar to :meth:`RDSDBInstance.wait_for_status`, but wait for
        DB instance to reach "available" status.
        """
        return self.wait_for_status(
            rds_client=rds_client,
            stop_status=RDSDBInstanceStatusEnum.available,
            delays=delays,
            timeout=timeout,
            error_status=list(
                RDSDBInstanceStatusGroupEnum.impossible_to_become_available
            ),
            indent=indent,
            verbose=verbose,
        )

    def wait_for_stopped(
        self,
        rds_client: "RDSClient",
        delays: T.Union[int, float] = 10,
        timeout: T.Union[int, float] = 300,
        indent: int = 0,
        verbose: bool = True,
    ) -> "RDSDBInstance":  # pragma: no cover
        """
        Similar to :meth:`RDSDBInstance.wait_for_status`, but wait for
        DB instance to reach "stopped" status.
        """
        return self.wait_for_status(
            rds_client=rds_client,
            stop_status=RDSDBInstanceStatusEnum.stopped,
            delays=delays,
            timeout=timeout,
            error_status=list(
                RDSDBInstanceStatusGroupEnum.impossible_to_become_stopped
            ),
            indent=indent,
            verbose=verbose,
        )

    # --------------------------------------------------------------------------
    # more constructor methods
    # --------------------------------------------------------------------------
    @classmethod
    def _yield_dict_from_describe_db_instances_response(
        cls,
        res: dict,
    ) -> T.Iterable["RDSDBInstance"]:
        db_instances = res.get("DBInstances", [])
        if len(db_instances):
            for db_instance_dict in db_instances:
                yield cls.from_dict(db_instance_dict)

    @classmethod
    def query(
        cls,
        rds_client: "RDSClient",
        db_instance_identifier: str = NOTHING,
        filters: T.List[dict] = NOTHING,
    ) -> "RDSDBInstanceIterProxy":
        """
        A wrapper around ``rds_client.describe_db_instances``.

        Multiple filters join with logic "AND", multiple values in a filter
        join with logic "OR".
        """

        def run():
            paginator = rds_client.get_paginator("describe_db_instances")
            kwargs = resolve_kwargs(
                DBInstanceIdentifier=db_instance_identifier,
                Filters=filters,
                PaginationConfig={
                    "MaxItems": 9999,
                    "PageSize": 100,
                },
            )
            if db_instance_identifier is not NOTHING:
                del kwargs["PaginationConfig"]
            response_iterator = paginator.paginate(**kwargs)
            for response in response_iterator:
                yield from cls._yield_dict_from_describe_db_instances_response(response)

        return RDSDBInstanceIterProxy(run())

    @classmethod
    def from_id(
        cls,
        rds_client: "RDSClient",
        db_identifier: str,
    ) -> T.Optional["RDSDBInstance"]:
        """
        Get RDS DB instance details by it's id.
        """
        return cls.query(
            rds_client,
            db_instance_identifier=db_identifier,
        ).one_or_none()

    @classmethod
    def from_tag_key_value(
        cls,
        rds_client: "RDSClient",
        key: str,
        value: str,
    ) -> "RDSDBInstanceIterProxy":
        """
        Query RDS DB Instance by tag key and value. This function only support
        single key, value pair filtering, if you want more advanced filtering,
        you can use the ``query`` method and do in-memory filtering.

        :param key: tag key
        :param value: tag value
        """

        def run():
            for db_inst in cls.query(rds_client):
                if db_inst.tags.get(key, "THIS_IS_IMPOSSIBLE_TO_MATCH") == value:
                    yield db_inst

        return RDSDBInstanceIterProxy(run())


class RDSDBInstanceIterProxy(IterProxy[RDSDBInstance]):
    """
    IterProxy for :class:`RDSDBInstance`.
    """

    pass


# TODO: implement RDS DB Cluster
# @dataclasses.dataclass
# class RDSDBCluster:
#     """
#     DB Cluster is only for Aurora DB.
#     """
#     pass


# class RDSDBClusterIterProxy(IterProxy[RDSDBCluster]):
#     """
#     IterProxy for RDSDBCluster.
#     """
#
#     pass


class RDSDBSnapshotStatusEnum(str, enum.Enum):
    """
    RDS DB snapshot status enum. The official document doesn't mention the exact
    string. But I found it is all lower case slugified.

    Reference:

    - https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_CreateSnapshot.html
    """

    creating = "creating"
    available = "available"


@dataclasses.dataclass
class RDSDBSnapshot:
    """
    Represent an RDS DB instance.

    See attributes explanation at:
    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds/client/describe_db_snapshots.html
    """

    # fmt: off
    db_snapshot_identifier: str = dataclasses.field(default=None)
    db_instance_identifier: T.Optional[str] = dataclasses.field(default=None)
    snapshot_create_time: T.Optional[datetime] = dataclasses.field(default=None)
    engine: T.Optional[str] = dataclasses.field(default=None)
    allocated_storage: T.Optional[int] = dataclasses.field(default=None)
    status: T.Optional[str] = dataclasses.field(default=None)
    port: T.Optional[int] = dataclasses.field(default=None)
    availability_zone: T.Optional[str] = dataclasses.field(default=None)
    vpc_id: T.Optional[str] = dataclasses.field(default=None)
    instance_create_time: T.Optional[datetime] = dataclasses.field(default=None)
    master_username: T.Optional[str] = dataclasses.field(default=None)
    engine_version: T.Optional[str] = dataclasses.field(default=None)
    license_model: T.Optional[str] = dataclasses.field(default=None)
    snapshot_type: T.Optional[str] = dataclasses.field(default=None)
    iops: T.Optional[str] = dataclasses.field(default=None)
    option_group_name: T.Optional[str] = dataclasses.field(default=None)
    percent_progress: T.Optional[int] = dataclasses.field(default=None)
    source_region: T.Optional[str] = dataclasses.field(default=None)
    source_db_snapshot_identifier: T.Optional[str] = dataclasses.field(default=None)
    storage_type: T.Optional[str] = dataclasses.field(default=None)
    tde_credential_arn: T.Optional[str] = dataclasses.field(default=None)
    encrypted: T.Optional[bool] = dataclasses.field(default=None)
    kms_key_id: T.Optional[str] = dataclasses.field(default=None)
    db_snapshot_arn: T.Optional[str] = dataclasses.field(default=None)
    timezone: T.Optional[str] = dataclasses.field(default=None)
    iam_database_authentication_enabled: T.Optional[bool] = dataclasses.field(default=None)
    processor_features: T.List[T.Dict[str, str]] = dataclasses.field(default_factory=list)
    dbi_resource_id: T.Optional[str] = dataclasses.field(default=None)
    tags: T.Dict[str, str] = dataclasses.field(default_factory=dict)
    original_snapshot_create_time: T.Optional[datetime] = dataclasses.field(default=None)
    snapshot_database_time: T.Optional[datetime] = dataclasses.field(default=None)
    snapshot_target: T.Optional[str] = dataclasses.field(default=None)
    storage_throughput: T.Optional[str] = dataclasses.field(default=None)
    db_system_id: T.Optional[str] = dataclasses.field(default=None)
    dedicated_log_volume: T.Optional[str] = dataclasses.field(default=None)
    multi_tenant: T.Optional[str] = dataclasses.field(default=None)
    data: T.Dict[str, T.Any] = dataclasses.field(default_factory=dict)
    # fmt: on

    @classmethod
    def from_dict(cls, dct: dict):
        # fmt: off
        return cls(
            db_snapshot_identifier=dct.get("DBSnapshotIdentifier"),
            db_instance_identifier=dct.get("DBInstanceIdentifier"),
            snapshot_create_time=dct.get("SnapshotCreateTime"),
            engine=dct.get("Engine"),
            allocated_storage=dct.get("AllocatedStorage"),
            status=dct.get("Status"),
            port=dct.get("Port"),
            availability_zone=dct.get("AvailabilityZone"),
            vpc_id=dct.get("VpcId"),
            instance_create_time=dct.get("InstanceCreateTime"),
            master_username=dct.get("MasterUsername"),
            engine_version=dct.get("EngineVersion"),
            license_model=dct.get("LicenseModel"),
            snapshot_type=dct.get("SnapshotType"),
            iops=dct.get("Iops"),
            option_group_name=dct.get("OptionGroupName"),
            percent_progress=dct.get("PercentProgress"),
            source_region=dct.get("SourceRegion"),
            source_db_snapshot_identifier=dct.get("SourceDBSnapshotIdentifier"),
            storage_type=dct.get("StorageType"),
            tde_credential_arn=dct.get("TdeCredentialArn"),
            encrypted=dct.get("Encrypted"),
            kms_key_id=dct.get("KmsKeyId"),
            db_snapshot_arn=dct.get("DBSnapshotArn"),
            timezone=dct.get("Timezone"),
            iam_database_authentication_enabled=dct.get("IAMDatabaseAuthenticationEnabled"),
            processor_features=dct.get("ProcessorFeatures", []),
            dbi_resource_id=dct.get("DbiResourceId"),
            tags={d["Key"]: d["Value"] for d in dct.get("TagList", [])},
            original_snapshot_create_time=dct.get("OriginalSnapshotCreateTime"),
            snapshot_database_time=dct.get("SnapshotDatabaseTime"),
            snapshot_target=dct.get("SnapshotTarget"),
            storage_throughput=dct.get("StorageThroughput"),
            db_system_id=dct.get("DBSystemId"),
            dedicated_log_volume=dct.get("DedicatedLogVolume"),
            multi_tenant=dct.get("MultiTenant"),
            data=dct.get(""),
        )
        # fmt: on

    def is_creating(self) -> bool:  # pragma: no cover
        """
        Check if the snapshot is in creating status.
        """
        return self.status == RDSDBSnapshotStatusEnum.creating.value

    def is_available(self) -> bool:  # pragma: no cover
        """
        Check if the snapshot is in available status.
        """
        return self.status == RDSDBSnapshotStatusEnum.available.value

    def wait_for_status(
        self,
        rds_client: "RDSClient",
        stop_status: T.Union[RDSDBSnapshotStatusEnum, T.List[RDSDBSnapshotStatusEnum]],
        gap: T.Union[int, float] = 1,
        delays: T.Union[int, float] = 10,
        timeout: T.Union[int, float] = 300,
        instant: bool = True,
        error_status: T.Optional[
            T.Union[RDSDBSnapshotStatusEnum, T.List[RDSDBSnapshotStatusEnum]]
        ] = None,
        indent: int = 0,
        verbose: bool = True,
    ) -> "RDSDBSnapshot":  # pragma: no cover
        """
        wait until the DB snapshot reaches the specified status defined in
        ``stop_status``. If reaches any of ``error_status ``, raise error.

        :param rds_client:
        :param stop_status: status to stop waiting
        :param gap: the time to wait before making first status check
        :param delays: delay between each check
        :param timeout: timeout in seconds
        :param instant: if True, then the first check is instant
        :param error_status: status to raise error
        :param indent: indent level for logging
        :param verbose: whether to print log

        :return: the :class:`RDSDBInstance` representing the latest status
            of DB instance.
        """
        if isinstance(stop_status, RDSDBInstanceStatusEnum):
            stop_status_set = {stop_status.value}
        else:
            stop_status_set = {status.value for status in RDSDBInstanceStatusEnum}
        if error_status is None:
            error_status_set = set()
        elif isinstance(error_status, RDSDBInstanceStatusEnum):
            error_status_set = {error_status.value}
        else:
            error_status_set = {status.value for status in RDSDBInstanceStatusEnum}

        if gap:
            time.sleep(gap)

        for attempt, elapse in Waiter(
            delays=delays,
            timeout=timeout,
            instant=instant,
            indent=indent,
            verbose=verbose,
        ):
            db_snapshot = self.from_id(rds_client, self.db_snapshot_identifier)
            if db_snapshot.status in stop_status_set:
                sys.stdout.write("\n")
                return db_snapshot
            elif db_snapshot.status in error_status_set:
                raise StatusError(f"stop because status reaches {db_snapshot.status!r}")
            else:
                pass

    def wait_for_available(
        self,
        rds_client,
        gap: T.Union[int, float] = 1,
        delays: T.Union[int, float] = 10,
        timeout: T.Union[int, float] = 300,
        indent: int = 0,
        verbose: bool = True,
    ) -> "RDSDBSnapshot":  # pragma: no cover
        """
        Similar to :meth:`RDSDBSnapshot.wait_for_status`, but wait for
        DB snapshot to reach "available" status.
        """
        return self.wait_for_status(
            rds_client=rds_client,
            stop_status=RDSDBSnapshotStatusEnum.available,
            gap=gap,
            delays=delays,
            timeout=timeout,
            indent=indent,
            verbose=verbose,
        )

    # --------------------------------------------------------------------------
    # more constructor methods
    # --------------------------------------------------------------------------
    @classmethod
    def _yield_dict_from_describe_db_snapshots_response(
        cls,
        res: dict,
    ) -> T.Iterable["RDSDBSnapshot"]:
        db_snapshots = res.get("DBSnapshots", [])
        if len(db_snapshots):
            for db_snapshot_dict in db_snapshots:
                yield cls.from_dict(db_snapshot_dict)

    @classmethod
    def query(
        cls,
        rds_client: "RDSClient",
        db_instance_identifier: str = NOTHING,
        db_snapshot_identifier: str = NOTHING,
        filters: T.List[dict] = NOTHING,
        snapshot_type: str = NOTHING,
        include_shared: bool = NOTHING,
        include_public: bool = NOTHING,
        dbi_resource_id: str = NOTHING,
    ) -> "RDSDBSnapshotIterProxy":
        """
        A wrapper around ``rds_client.describe_db_snapshots``.

        Multiple filters join with logic "AND", multiple values in a filter
        join with logic "OR".
        """

        def run():
            paginator = rds_client.get_paginator("describe_db_snapshots")
            kwargs = resolve_kwargs(
                DBInstanceIdentifier=db_instance_identifier,
                DBSnapshotIdentifier=db_snapshot_identifier,
                Filters=filters,
                SnapshotType=snapshot_type,
                IncludeShared=include_shared,
                IncludePublic=include_public,
                DbiResourceId=dbi_resource_id,
                PaginationConfig={
                    "MaxItems": 9999,
                    "PageSize": 100,
                },
            )
            if db_snapshot_identifier is not NOTHING:
                del kwargs["PaginationConfig"]
            response_iterator = paginator.paginate(**kwargs)
            for response in response_iterator:
                yield from cls._yield_dict_from_describe_db_snapshots_response(response)

        return RDSDBSnapshotIterProxy(run())

    @classmethod
    def from_id(
        cls,
        rds_client: "RDSClient",
        db_snapshot_identifier: str,
    ) -> T.Optional["RDSDBInstance"]:
        """
        Get RDS DB snapshot details by it's id.
        """
        return cls.query(
            rds_client,
            db_snapshot_identifier=db_snapshot_identifier,
        ).one_or_none()

    @classmethod
    def from_tag_key_value(
        cls,
        rds_client: "RDSClient",
        key: str,
        value: str,
    ) -> "RDSDBSnapshotIterProxy":
        """
        Query RDS DB snapshot by tag key and value. This function only support
        single key, value pair filtering, if you want more advanced filtering,
        you can use the ``query`` method and do in-memory filtering.

        :param key: tag key
        :param value: tag value
        """

        def run():
            for db_snap in cls.query(rds_client):
                if (
                    db_snap.tags.get(key, "THIS_IS_IMPOSSIBLE_TO_MATCH") == value
                ):  # pragma: no cover
                    yield db_snap

        return RDSDBSnapshotIterProxy(run())


class RDSDBSnapshotIterProxy(IterProxy[RDSDBSnapshot]):
    """
    IterProxy for :class:`RDSDBSnapshot`.
    """

    pass


# TODO: implement RDS DB Cluster
# @dataclasses.dataclass
# class RDSDBClusterSnapshot:
#     """
#     """
#     pass


# class RDSDBClusterSnapshotIterProxy(IterProxy[RDSDBClusterSnapshot]):
#     """
#     IterProxy for RDSDBClusterSnapshot.
#     """
#
#     pass
