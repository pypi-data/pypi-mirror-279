# -*- coding: utf-8 -*-


def test():
    from simple_aws_rds import api

    # top level API
    _ = api.exc
    _ = api.StatusError
    _ = api.RDSDBInstanceStatusEnum
    _ = api.RDSDBInstanceStatusGroupEnum
    _ = api.RDSDBInstance
    _ = api.RDSDBInstanceIterProxy
    _ = api.RDSDBSnapshotStatusEnum
    _ = api.RDSDBSnapshot
    _ = api.RDSDBSnapshotIterProxy

    # attribute and method
    _ = api.RDSDBInstance.from_dict
    _ = api.RDSDBInstance.is_available
    _ = api.RDSDBInstance.is_backing_up
    _ = api.RDSDBInstance.is_configuring_enhanced_monitoring
    _ = api.RDSDBInstance.is_configuring_iam_database_auth
    _ = api.RDSDBInstance.is_configuring_log_exports
    _ = api.RDSDBInstance.is_converting_to_vpc
    _ = api.RDSDBInstance.is_creating
    _ = api.RDSDBInstance.is_delete_precheck
    _ = api.RDSDBInstance.is_deleting
    _ = api.RDSDBInstance.is_failed
    _ = api.RDSDBInstance.is_inaccessible_encryption_credentials
    _ = api.RDSDBInstance.is_inaccessible_encryption_credentials_recoverable
    _ = api.RDSDBInstance.is_incompatible_network
    _ = api.RDSDBInstance.is_incompatible_option_group
    _ = api.RDSDBInstance.is_incompatible_parameters
    _ = api.RDSDBInstance.is_incompatible_restore
    _ = api.RDSDBInstance.is_insufficient_capacity
    _ = api.RDSDBInstance.is_maintenance
    _ = api.RDSDBInstance.is_modifying
    _ = api.RDSDBInstance.is_moving_to_vpc
    _ = api.RDSDBInstance.is_rebooting
    _ = api.RDSDBInstance.is_resetting_master_credentials
    _ = api.RDSDBInstance.is_renaming
    _ = api.RDSDBInstance.is_restore_error
    _ = api.RDSDBInstance.is_starting
    _ = api.RDSDBInstance.is_stopped
    _ = api.RDSDBInstance.is_stopping
    _ = api.RDSDBInstance.is_storage_full
    _ = api.RDSDBInstance.is_storage_optimization
    _ = api.RDSDBInstance.is_upgrading
    _ = api.RDSDBInstance.is_ready_to_start
    _ = api.RDSDBInstance.is_ready_to_stop
    _ = api.RDSDBInstance.is_end
    _ = api.RDSDBInstance.is_in_transition
    _ = api.RDSDBInstance.start_db_instance
    _ = api.RDSDBInstance.stop_db_instance
    _ = api.RDSDBInstance.delete_db_instance
    _ = api.RDSDBInstance.wait_for_status
    _ = api.RDSDBInstance.wait_for_available
    _ = api.RDSDBInstance.wait_for_stopped
    _ = api.RDSDBInstance.query
    _ = api.RDSDBInstance.from_id
    _ = api.RDSDBInstance.from_tag_key_value

    _ = api.RDSDBSnapshot.from_dict
    _ = api.RDSDBSnapshot.is_creating
    _ = api.RDSDBSnapshot.is_available
    _ = api.RDSDBSnapshot.wait_for_status
    _ = api.RDSDBSnapshot.wait_for_available
    _ = api.RDSDBSnapshot.query
    _ = api.RDSDBSnapshot.from_id
    _ = api.RDSDBSnapshot.from_tag_key_value


if __name__ == "__main__":
    from simple_aws_rds.tests import run_cov_test

    run_cov_test(__file__, "simple_aws_rds.api", preview=False)
