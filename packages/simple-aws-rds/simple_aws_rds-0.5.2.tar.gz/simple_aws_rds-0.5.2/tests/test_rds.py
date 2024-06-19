# -*- coding: utf-8 -*-

import pytest
import moto
from boto_session_manager import BotoSesManager

from simple_aws_rds.rds import (
    RDSDBInstanceStatusEnum,
    RDSDBInstanceStatusGroupEnum,
    RDSDBInstance,
    RDSDBSnapshotStatusEnum,
    RDSDBSnapshot,
    StatusError,
)


class TestRDSDBInstanceStatusGroupEnum:
    def test(self):
        _ = RDSDBInstanceStatusGroupEnum.impossible_to_become_available
        _ = RDSDBInstanceStatusGroupEnum.impossible_to_become_stopped


class TestRds:
    mock_rds = None
    bsm: BotoSesManager = None

    @classmethod
    def setup_rds_resources(cls):
        cls.inst_id_1 = cls.bsm.rds_client.create_db_instance(
            DBInstanceIdentifier="db-inst-1",
            DBInstanceClass="db.t2.micro",
            Engine="mysql",
        )["DBInstance"]["DBInstanceIdentifier"]

        cls.inst_id_2 = cls.bsm.rds_client.create_db_instance(
            DBInstanceIdentifier="db-inst-2",
            DBInstanceClass="db.t2.medium",
            Engine="mysql",
            Tags=[
                dict(Key="Name", Value="my-db"),
            ],
        )["DBInstance"]["DBInstanceIdentifier"]

        cls.snap_id_1 = cls.bsm.rds_client.create_db_snapshot(
            DBInstanceIdentifier=cls.inst_id_1,
            DBSnapshotIdentifier="db-snap-1-1",
        )["DBSnapshot"]["DBSnapshotIdentifier"]

        cls.snap_id_2 = cls.bsm.rds_client.create_db_snapshot(
            DBInstanceIdentifier=cls.inst_id_2,
            DBSnapshotIdentifier="db-snap-2-1",
        )["DBSnapshot"]["DBSnapshotIdentifier"]

    @classmethod
    def setup_class(cls):
        cls.mock_rds = moto.mock_rds()
        cls.mock_rds.start()
        cls.bsm = BotoSesManager(region_name="us-east-1")
        cls.setup_rds_resources()

    @classmethod
    def teardown_class(cls):
        cls.mock_rds.stop()

    def _test_db_instance(self):
        inst_id_list = [
            self.inst_id_1,
            self.inst_id_2,
        ]
        for inst_id in inst_id_list:
            db_inst = RDSDBInstance.from_id(self.bsm.rds_client, inst_id)
            assert db_inst.is_available() is True
            assert db_inst.is_stopped() is False
            assert db_inst.is_ready_to_start() is False
            assert db_inst.is_ready_to_stop() is True
            assert db_inst.is_end() is True
            assert db_inst.is_in_transition() is False
            assert db_inst.id == inst_id

        db_inst_list = RDSDBInstance.query(self.bsm.rds_client).all()
        assert len(db_inst_list) == 2

        db_inst_list = RDSDBInstance.from_tag_key_value(
            self.bsm.rds_client, key="Name", value="my-db"
        ).all()
        assert len(db_inst_list) == 1
        db_inst = db_inst_list[0]
        assert db_inst.id == self.inst_id_2
        assert db_inst.tags["Name"] == "my-db"

        db_inst = RDSDBInstance.from_id(self.bsm.rds_client, self.inst_id_1)
        db_inst.stop_db_instance(self.bsm.rds_client)
        db_inst = RDSDBInstance.from_id(self.bsm.rds_client, self.inst_id_1)
        assert db_inst.is_available() is False
        assert db_inst.is_stopped() is True

        db_inst.start_db_instance(self.bsm.rds_client)
        db_inst = RDSDBInstance.from_id(self.bsm.rds_client, self.inst_id_1)
        assert db_inst.is_stopped() is False
        assert db_inst.is_available() is True

        db_inst_list = RDSDBInstance.from_tag_key_value(
            self.bsm.rds_client, key="Env", value="sandbox"
        ).all()
        assert len(db_inst_list) == 0

    def _test_wait_for_status(self):
        db_inst = RDSDBInstance.from_id(self.bsm.rds_client, self.inst_id_1)
        assert db_inst.is_available() is True
        with pytest.raises(StatusError):
            db_inst.wait_for_stopped(
                rds_client=self.bsm.rds_client,
                verbose=False,
            )

        db_inst.stop_db_instance(self.bsm.rds_client)
        new_db_inst = db_inst.wait_for_status(
            rds_client=self.bsm.rds_client,
            stop_status=RDSDBInstanceStatusEnum.stopped,
            verbose=False,
        )
        assert new_db_inst.is_stopped() is True
        with pytest.raises(StatusError):
            db_inst.wait_for_available(
                rds_client=self.bsm.rds_client,
                verbose=False,
            )

    def _test_db_snapshot(self):
        snap = RDSDBSnapshot.from_id(self.bsm.rds_client, self.snap_id_1)
        assert snap.is_available() is True

        snap = RDSDBSnapshot(db_snapshot_identifier=self.snap_id_1).wait_for_available(
            rds_client=self.bsm.rds_client, verbose=False
        )
        assert snap.is_available() is True

        snap_list = RDSDBSnapshot.from_tag_key_value(
            self.bsm.rds_client, key="Env", value="sandbox"
        ).all()
        assert len(snap_list) == 0

    def _test_delete_db_instance(self):
        db_inst = RDSDBInstance.from_id(self.bsm.rds_client, self.inst_id_1)
        db_inst.delete_db_instance(self.bsm.rds_client)
        try:
            RDSDBInstance.from_id(self.bsm.rds_client, self.inst_id_1)
        except Exception as e:
            assert "not found" in str(e)

    def test(self):
        # these test has to run in sequence, the next test depends on the state
        # of previous one
        self._test_db_instance()
        self._test_wait_for_status()
        self._test_db_snapshot()
        self._test_delete_db_instance()


if __name__ == "__main__":
    from simple_aws_rds.tests import run_cov_test

    run_cov_test(__file__, "simple_aws_rds.rds", preview=False)
