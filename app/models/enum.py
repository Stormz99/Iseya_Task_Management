from enum import Enum

class PriorityEnum(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    VERY_URGENT = "very_urgent"

class StatusEnum(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"

class RoleEnum(str, Enum):
    ADMIN = "admin"
    USER = "user"
