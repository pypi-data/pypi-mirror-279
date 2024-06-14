from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Offsets:
    # in radians in FLU
    roll: Optional[float] = None
    pitch: Optional[float] = None
    yaw: Optional[float] = None
    forward: Optional[float] = None
    left: Optional[float] = None
    up: Optional[float] = None


@dataclass
class Camera:
    # This will become the name of frame-id, ros topic and webrtc stream
    name: str
    # Used to order the stream in the UI
    order: int
    # An array of gstream source / transform elements e.g.
    # ["v4l2src", "video/x-raw, format=RGB,width=1920,height=1080"]
    elements: List[str]

    pixel_width: int
    pixel_height: int
    # Published ros topic names
    camera_frame_topic: Optional[str]
    camera_info_topic: Optional[str]
    # Camera intrinsics and distortion parameters from callibration
    k_intrinsic: Optional[List[float]] = field(
        default_factory=lambda: [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0]
    )
    distortion_parameters: Optional[List[float]] = field(
        default_factory=lambda: [0.0, 0.0, 0.0, 0.0, 0.0]
    )
    distortion_model: str = "plumb_bob"
    # The camera's position relative to the vessel base_link
    offsets: Optional[Offsets] = None
    type: str = "color"
    ros_throttle_time: float = 0.0000001
    # Whether to undistort the image in gstreamer pipeline before publishing
    undistort_image: bool = False


@dataclass
class CameraOverride:
    # This will become the name of frame-id, ros topic and webrtc stream
    name: Optional[str]
    order: Optional[int]
    # An array of gstream source / transform elements e.g.
    # ["v4l2src", "video/x-raw, format=RGB,width=1920,height=1080"]
    elements: Optional[List[str]]
    pixel_width: Optional[int]
    pixel_height: Optional[int]
    # Published ros topic names
    camera_frame_topic: Optional[str]
    camera_info_topic: Optional[str]
    # Camera intrinsics and distortion parameters from callibration
    k_intrinsic: Optional[List[float]] = None
    distortion_parameters: Optional[List[float]] = None
    distortion_model: str = "plumb_bob"
    # The camera's position relative to the vessel base_link
    offsets: Optional[Offsets] = None
    type: Optional[str] = "color"
    ros_throttle_time: Optional[float] = 0.0000001
    # Whether to undistort the image in gstreamer pipeline before publishing
    undistort_image: Optional[bool] = False


@dataclass
class GreenstreamConfig:
    cameras: List[Camera]
    camera_overrides: Optional[List[Optional[CameraOverride]]] = None
    signalling_server_port: int = 8443
    namespace: str = ""  # eg. vessel_1
    ui_port: int = 8080
    mode: str = "simulator"
    variant: str = ""
