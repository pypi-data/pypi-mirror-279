from datetime import datetime
from uuid import UUID

from oqc_cloud.common import types
from oqc_cloud.common.types import Lease, ScheduledWindow, Tenancy
from qcaas_common.enums import LeaseType, WindowState
from qcaas_common.logger import get_logger

log = get_logger(__name__)


def id_str_to_uuid(id: str) -> UUID:
    try:
        if isinstance(id, UUID):
            return id
        else:
            return UUID(id, version=4)
    except ValueError as ex:
        log.error(f"Converting {id} to UUID failed.")
        raise ex


def target_to_qpu(target: str) -> types.Qpu:
    try:
        if isinstance(target, types.Qpu):
            return target
        else:
            return types.Qpu(str(target))
    except ValueError as ex:
        log.error(f"Converting {target} to Qpu failed.")
        raise ex


def json_to_scheduled_window(window_dict: dict):
    try:
        start_time = string_to_datetime(window_dict.get("start_time"))
        end_time = string_to_datetime(window_dict.get("end_time"))
        lease = json_to_lease(window_dict.get("lease"))
        description = (
            WindowState(window_dict.get("description", ""))
            if window_dict.get("description", False)
            else None
        )
        return ScheduledWindow(start_time, end_time, lease, description)
    except ValueError as ex:
        log.error(f"Converting {window_dict} to ScheduledWindow failed.")
        raise ex


def string_to_datetime(date: str):
    try:
        if isinstance(date, datetime):
            return date
        else:
            return datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    except ValueError as ex:
        log.error(f"Converting {date} to datetime failed.")
        raise ex


def json_to_lease(lease_dict: dict):
    try:
        type = LeaseType(int(lease_dict.get("type", 0)))
        name = lease_dict.get("name", "")
        tenancies = [
            Tenancy(tenant.get("lease_holder_name", ""), int(tenant.get("priority", 1)))
            for tenant in lease_dict.get("tenancies", [])
        ]
        return Lease(type, name, tenancies)
    except ValueError as ex:
        log.error(f"Converting {lease_dict} to Lease failed.")
        raise ex
