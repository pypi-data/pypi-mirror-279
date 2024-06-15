from typing import TypedDict


class BagGripperDetails(TypedDict):
    """Dictionary representing the details of a bag gripper

    Args:
        TypedDict (TypedDict): _description_
    """

    name: str
    uuid: str
    controllerId: str
    device: int
    ip: str
    closeInPin: int
    openInPin: int
    closeOutPin: int
    openOutPin: int
