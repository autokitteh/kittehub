"""Common data types."""

from dataclasses import dataclass


@dataclass
class CurrentState:
    """Current deployment state"""

    image: str

    desired_replicas: int
    available_replicas: int
    unavailable_replicas: int
    updated_replicas: int
    ready_replicas: int


@dataclass
class Deployment:
    """Single deployment row"""

    row_num: int

    name: str
    slack: list[str]
    op: str
    status: str

    desired_image: str
    desired_replicas: int | None
