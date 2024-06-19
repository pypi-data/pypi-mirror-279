from enum import Enum, Flag, auto


class _AutoNameEnum(Enum):
    @staticmethod
    def _generate_next_value_(name, start, count, last_value):
        return name


class ReceiverMode(Enum):
    COMPILE_AND_EXECUTE = "compile-and-execute"
    COMPILE_ONLY = "compile-only"
    EXECUTE_ONLY = "execute-only"


class Event(_AutoNameEnum):
    # TODO: Discussion regarding upgrading Event enums
    SERVER_RECEIVED = auto()
    SERVER_ENQUEUED = auto()
    SERVER_DEQUEUED = auto()
    RECEIVER_DEQUEUED = auto()
    RECEIVER_TO_COMPILER = auto()
    RECEIVER_FROM_COMPILER = auto()
    RECEIVER_ENQUEUED = auto()
    COMPILER_ENQUEUED = auto()
    COMPILER_DEQUEUED = auto()
    EXECUTOR_ENQUEUED = auto()
    EXECUTOR_DEQUEUED = auto()


class Status(_AutoNameEnum):
    CREATED = auto()
    SUBMITTED = auto()
    FAILED_DECRYPTION = auto()
    RUNNING = auto()
    COMPLETED = auto()
    FAILED = auto()
    COMPILED = auto()
    CANCELLED = auto()
    EXPIRED = auto()

    @staticmethod
    def from_str(text: str):
        return Status[text.upper()]


class ClientTaskStatus(Enum):
    UNKNOWN = "UNKNOWN"
    CREATED = "CREATED"
    SUBMITTED = "SUBMITTED"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"
    EXPIRED = "EXPIRED"


class QpuConnectionStatus(_AutoNameEnum):
    AVAILABLE = auto()
    NOTCONNECTED = auto()
    OFFLINE = auto()
    UNKNOWN = auto()

    @staticmethod
    def from_str(text: str):
        return QpuConnectionStatus[text.upper()]


def _with_all_flags(enumeration):
    enums = enumeration(0)  # in case NONE is not defined
    for name, member in enumeration.__members__.items():
        enums |= member
    enumeration.All = enums
    return enumeration


@_with_all_flags
class TaskInfo(Flag):
    WithStatus = auto()
    WithResults = auto()
    WithErrors = auto()
    WithExecutionMetaData = auto()
    WithProgram = auto()
    WithMetaData = auto()
    WithEventTimes = auto()


class UserInfo(Flag):
    WithRole = auto()
    WithMetaData = auto()
    WithPasswordMetaData = auto()
    All = WithRole | WithMetaData | WithPasswordMetaData


class _SerialisableFlag(Flag):
    def to_str(self):
        set_flags = [val._name_ for val in type(self) if val in self]
        return "|".join(set_flags)

    @classmethod
    def from_str(cls, s):
        options = s.split("|")

        out = None
        for option in options:
            temp = getattr(cls, option, None)
            if isinstance(temp, cls):
                if isinstance(out, cls):
                    out |= temp
                else:
                    out = temp
        return out


class UserPermission(_SerialisableFlag):
    WindowAdmin = auto()
    WindowReader = auto()
    User = auto()
    WindowManager = auto()
    ScheduleManager = auto()
    TenancyManager = auto()
    SchedulerAdmin = auto()
    ServerAdmin = auto()
    Admin = auto()  # Legacy (use ServerAdmin instead)
    Broadcaster = auto()


class CancelTask(Flag):
    WhileRunning = auto()
    AfterCancelled = auto()


class HardwareMode(Enum):
    Connect = auto()
    HardDisconnect = auto()
    SoftDisconnect = auto()


class TriggerType(Enum):
    QUEUE_KEY = "queue"
    QUERY_KEY = "query"
    CANCEL_KEY = "cancel_task_id"
    COMMAND_KEY = "command_key"
    CONN_KEY = "connect_key"
    HARD_DISCONN_KEY = "hard_hardware_disconnect_key"
    SOFT_DISCONN_KEY = "soft_hardware_disconnect_key"
    HARDWARE_RELOAD_KEY = "reload_hardware_key"


class WindowState(Enum):
    CURRENT = "CURRENT"
    NEXT = "NEXT"
    FUTURE = "FUTURE"


class LeaseType(Enum):
    ALL_PRIORITY = auto()
    ANY_PRIORITY = auto()
    ANY_AVAILABILITY = auto()
    EXCLUSIVE = auto()


class HardwareType(_AutoNameEnum):
    ECHO = auto()
    QUTIP = auto()
    LIVE = auto()
    RTCS = auto()
    QISKITAER = auto()


class DeviceEngine(_AutoNameEnum):
    LEGACY = auto()
    ARBSEQ = auto()
