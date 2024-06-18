from abc import ABC, abstractmethod
from collections.abc import AsyncGenerator, Awaitable, Coroutine
from typing import Any, Callable, Generic, Optional, TypeVar, Union, overload, runtime_checkable

from PIL import Image
from reactivex import Observable
from typing_extensions import (
    Literal,
    NotRequired,
    Protocol,
    TypedDict,
)

Callback = Union[
    Callable[..., Any],
    Callable[..., Coroutine[Any, Any, Any]],
]


# schema
JsonSchemaType = Literal["string", "number", "boolean", "object", "array"]


class JsonBaseSchema(TypedDict):
    key: NotRequired[Optional[str]]
    title: NotRequired[Optional[str]]
    description: NotRequired[Optional[str]]
    required: NotRequired[Optional[bool]]
    readonly: NotRequired[Optional[bool]]
    placeholder: NotRequired[Optional[str]]
    hidden: NotRequired[Optional[bool]]
    group: NotRequired[Optional[str]]
    defaultValue: NotRequired[Optional[Union[str, int, bool]]]


class PluginJsonBaseSchema(JsonBaseSchema):
    store: NotRequired[Optional[bool]]
    onSet: NotRequired[Callable[[Any, Any], Awaitable[Union[None, Any]]]]
    onGet: NotRequired[Callable[[], Awaitable[Union[Any, None]]]]


class PluginJsonSchemaString(PluginJsonBaseSchema):
    type: Literal["string"]
    format: NotRequired[str]
    minLength: NotRequired[int]
    maxLength: NotRequired[int]


class PluginJsonSchemaNumber(PluginJsonBaseSchema):
    type: Literal["number"]
    minimum: NotRequired[int]
    maximum: NotRequired[int]
    step: NotRequired[float]


class PluginJsonSchemaBoolean(PluginJsonBaseSchema):
    type: Literal["boolean"]


class PluginJsonSchemaEnum(PluginJsonBaseSchema):
    type: Literal["string"]
    enum: list[str]
    multiple: NotRequired[bool]


class PluginJsonSchemaObject(PluginJsonBaseSchema):
    type: Literal["object"]
    opened: NotRequired[bool]
    properties: NotRequired["PluginJsonSchemaForm"]


PluginJsonSchema = Union[
    PluginJsonSchemaString,
    PluginJsonSchemaNumber,
    PluginJsonSchemaBoolean,
    PluginJsonSchemaEnum,
    PluginJsonSchemaObject,
]


PluginJsonSchemaForm = dict[str, PluginJsonSchema]


class PluginRootSchema(TypedDict):
    schema: PluginJsonSchemaForm


class JsonSchemaString(JsonBaseSchema):
    type: Literal["string"]
    format: NotRequired[str]
    minLength: NotRequired[int]
    maxLength: NotRequired[int]


class JsonSchemaNumber(JsonBaseSchema):
    type: Literal["number"]
    minimum: NotRequired[int]
    maximum: NotRequired[int]
    step: NotRequired[float]


class JsonSchemaBoolean(JsonBaseSchema):
    type: Literal["boolean"]


class JsonSchemaEnum(JsonBaseSchema):
    type: Literal["string"]
    enum: list[str]
    multiple: NotRequired[bool]


class JsonSchemaObject(JsonBaseSchema):
    type: Literal["object"]
    opened: NotRequired[bool]
    properties: NotRequired["JsonSchemaForm"]


class JsonSchemaButton(TypedDict):
    label: str
    onSubmit: str


class JsonSchemaObjectWithButtons(JsonSchemaObject):
    buttons: NotRequired[tuple[JsonSchemaButton, NotRequired[JsonSchemaButton]]]


class JsonSchemaAnyOf(TypedDict):
    anyOf: list["JsonSchema"]


class JsonSchemaArray(JsonBaseSchema):
    type: Literal["array"]
    opened: NotRequired[bool]
    items: NotRequired[Union["JsonSchema", JsonSchemaAnyOf]]


JsonSchema = Union[
    JsonSchemaString,
    JsonSchemaNumber,
    JsonSchemaBoolean,
    JsonSchemaEnum,
    JsonSchemaObject,
    JsonSchemaObjectWithButtons,
    JsonSchemaArray,
]


JsonSchemaForm = dict[str, JsonSchema]


class RootSchema(TypedDict):
    schema: JsonSchemaForm


class SchemaConfig(TypedDict):
    rootSchema: PluginRootSchema
    config: dict[str, Union[str, int, bool]]


# camera object
class Go2RtcFFMPEGSource(TypedDict):
    aac: str
    opus: str


class Go2RtcWSSource(TypedDict):
    webrtc: str


class Go2RtcRTSPSource(TypedDict):
    single: str
    default: str
    mp4: str


class Go2RtcEndpoint(TypedDict):
    webrtc: str
    mse: str
    lmp4: str
    mmp4: str
    mp4: str
    mp4Snapshot: str
    jpegSnapshot: str
    lHlsTs: str
    lHlsFmp4: str
    mHlsFmp4: str
    mjpeg: str
    mjpegHtml: str


class StreamUrls(TypedDict):
    ws: Go2RtcWSSource
    rtsp: Go2RtcRTSPSource
    transcoded: Go2RtcFFMPEGSource
    www: Go2RtcEndpoint


class CameraInput(TypedDict):
    _id: str
    name: str
    roles: list["CameraRoles"]
    urls: StreamUrls


CameraRoles = Literal["detect", "record", "stream", "snapshot", "none"]

CameraExtension = Literal[
    "hub",
    "prebuffer",
    "motionDetection",
    "objectDetection",
    "audioDetection",
    "ptz",
    "intercom",
]

Point = tuple[float, float]

ZoneType = Literal["intersect", "contain"]

ZoneFilter = Literal["include", "exclude"]


class DetectionZone(TypedDict):
    name: str
    points: list[Point]
    type: ZoneType
    filter: ZoneFilter
    classes: list[str]
    isPrivacyMask: bool


class CameraInformation(TypedDict):
    model: str
    manufacturer: str
    hardware: str
    serialNumber: str
    firmwareVersion: str
    supportUrl: str


class MotionDetectionSettings(TypedDict):
    timeout: int


class ObjectDetectionSettings(TypedDict):
    confidence: float


class CameraActivitySettings(TypedDict):
    motion: MotionDetectionSettings
    object: ObjectDetectionSettings


CameraType = Literal["camera", "doorbell"]

CameraFrameWorker = Literal["pillow", "sharp", "wasm"]


class Camera(TypedDict):
    _id: str
    nativeId: NotRequired[str]
    pluginId: str
    name: str
    disabled: bool
    isCloud: bool
    hasLight: bool
    hasSiren: bool
    hasBinarySensor: bool
    hasBattery: bool
    info: CameraInformation
    type: CameraType
    activityZones: list[DetectionZone]
    activitySettings: CameraActivitySettings
    hasAudioDetector: bool
    hasMotionDetector: bool
    hasObjectDetector: bool
    hasPrebuffer: bool
    hasIntercom: bool
    hasPtz: bool
    sources: list[CameraInput]
    frameWorker: Literal["pillow", "sharp", "wasm"]


CameraPublicProperties = Literal[
    "_id",
    "nativeId",
    "pluginId",
    "name",
    "disabled",
    "isCloud",
    "hasLight",
    "hasSiren",
    "hasBinarySensor",
    "hasBattery",
    "info",
    "type",
    "activityZones",
    "activitySettings",
    "hasAudioDetector",
    "hasMotionDetector",
    "hasObjectDetector",
    "hasPrebuffer",
    "hasIntercom",
    "hasPtz",
    "sources",
    "frameWorker",
]

PropertyValue = Union[
    str,
    bool,
    CameraInformation,
    CameraType,
    CameraActivitySettings,
    list[DetectionZone],
    list[CameraInput],
]


# camera device
ObjectClasses = Literal[
    "person",
    "bicycle",
    "car",
    "motorcycle",
    "airplane",
    "bus",
    "train",
    "truck",
    "boat",
    "traffic light",
    "fire hydrant",
    "stop sign",
    "parking meter",
    "bench",
    "bird",
    "cat",
    "dog",
    "horse",
    "sheep",
    "cow",
    "elephant",
    "bear",
    "zebra",
    "giraffe",
    "backpack",
    "umbrella",
    "handbag",
    "tie",
    "suitcase",
    "frisbee",
    "skis",
    "snowboard",
    "sports ball",
    "kite",
    "baseball bat",
    "baseball glove",
    "skateboard",
    "surfboard",
    "tennis racket",
    "bottle",
    "wine glass",
    "cup",
    "fork",
    "knife",
    "spoon",
    "bowl",
    "banana",
    "apple",
    "sandwich",
    "orange",
    "broccoli",
    "carrot",
    "hot dog",
    "pizza",
    "donut",
    "cake",
    "chair",
    "couch",
    "potted plant",
    "bed",
    "dining table",
    "toilet",
    "tv",
    "laptop",
    "mouse",
    "remote",
    "keyboard",
    "cell phone",
    "microwave",
    "oven",
    "toaster",
    "sink",
    "refrigerator",
    "book",
    "clock",
    "vase",
    "scissors",
    "teddy bear",
    "hair drier",
    "toothbrush",
    "motion",
]


class Detection(TypedDict):
    id: NotRequired[str]
    label: ObjectClasses
    confidence: float
    boundingBox: tuple[float, float, float, float]
    inputWidth: int
    inputHeight: int
    origWidth: int
    origHeight: int


class BaseStateLight(TypedDict):
    timestamp: int
    lastEvent: NotRequired[Optional["LightStateWithoutLastEvent"]]


class BaseStateMotion(TypedDict):
    timestamp: int
    lastEvent: NotRequired[Optional["MotionStateWithoutLastEvent"]]


class BaseStateAudio(TypedDict):
    timestamp: int
    lastEvent: NotRequired[Optional["AudioStateWithoutLastEvent"]]


class BaseStateObject(TypedDict):
    timestamp: int
    lastEvent: NotRequired[Optional["ObjectStateWithoutLastEvent"]]


class BaseStateDoorbell(TypedDict):
    timestamp: int
    lastEvent: NotRequired[Optional["DoorbellStateWithoutLastEvent"]]


class BaseStateSiren(TypedDict):
    timestamp: int
    lastEvent: NotRequired[Optional["SirenStateWithoutLastEvent"]]


class BaseStateBattery(TypedDict):
    timestamp: int
    lastEvent: NotRequired[Optional["BatteryStateWithoutLastEvent"]]


class BaseStateWithoutLastEvent(TypedDict):
    timestamp: int


class MotionSetEvent(TypedDict):
    state: NotRequired[bool]
    detections: list[Detection]


class AudioSetEvent(TypedDict):
    state: bool
    db: NotRequired[Optional[int]]


class ObjectSetEvent(TypedDict):
    detections: list[Detection]


class LightSetEvent(TypedDict):
    state: bool


class DoorbellSetEvent(TypedDict):
    state: bool


class SirenSetEvent(TypedDict):
    state: bool
    level: NotRequired[Optional[int]]


class BatterySetEvent(TypedDict):
    level: int
    charging: NotRequired[Optional[bool]]
    lowBattery: NotRequired[Optional[bool]]


class LightState(BaseStateLight, LightSetEvent): ...


class LightStateWithoutLastEvent(BaseStateWithoutLastEvent, LightSetEvent): ...


class MotionState(BaseStateMotion, MotionSetEvent): ...


class MotionStateWithoutLastEvent(BaseStateWithoutLastEvent, MotionSetEvent): ...


class AudioState(BaseStateAudio, AudioSetEvent): ...


class AudioStateWithoutLastEvent(BaseStateWithoutLastEvent, AudioSetEvent): ...


class DoorbellState(BaseStateDoorbell, DoorbellSetEvent): ...


class DoorbellStateWithoutLastEvent(BaseStateWithoutLastEvent, DoorbellSetEvent): ...


class SirenState(BaseStateSiren, SirenSetEvent): ...


class SirenStateWithoutLastEvent(BaseStateWithoutLastEvent, SirenSetEvent): ...


class ObjectState(BaseStateObject, ObjectSetEvent): ...


class ObjectStateWithoutLastEvent(BaseStateWithoutLastEvent, ObjectSetEvent): ...


class BatteryState(BaseStateBattery, BatterySetEvent): ...


class BatteryStateWithoutLastEvent(BaseStateWithoutLastEvent, BatterySetEvent): ...


class FrameState(MotionState):
    frame: bytes


T = TypeVar(
    "T",
    LightState,
    MotionState,
    AudioState,
    DoorbellState,
    SirenState,
    ObjectState,
    BatteryState,
)


class StateValues(Protocol):
    light: LightState
    motion: MotionState
    audio: AudioState
    object: ObjectState
    doorbell: DoorbellState
    siren: SirenState
    battery: BatteryState


class SetValues(Protocol):
    light: LightSetEvent
    motion: MotionSetEvent
    audio: AudioSetEvent
    object: ObjectSetEvent
    doorbell: DoorbellSetEvent
    siren: SirenSetEvent
    battery: BatterySetEvent


CameraStateCallbacks = dict[str, Callable[[T], None]]

StateValue = Union[
    LightState,
    MotionState,
    AudioState,
    DoorbellState,
    SirenState,
    ObjectState,
    BatteryState,
]

SetValue = Union[
    LightSetEvent,
    MotionSetEvent,
    AudioSetEvent,
    DoorbellSetEvent,
    SirenSetEvent,
    BatterySetEvent,
    ObjectSetEvent,
]

StateNames = Literal["light", "motion", "audio", "doorbell", "siren", "battery", "object"]

OnChangeCallback = Callable[[T, T], None]


class AudioStreamOptions(TypedDict):
    enabled: NotRequired[bool]
    codec: NotRequired[str]
    bitrate: NotRequired[int]
    sampleRate: NotRequired[int]


class VideoStreamOptions(TypedDict):
    codec: NotRequired[str]
    width: NotRequired[int]
    height: NotRequired[int]
    bitrate: NotRequired[int]
    fps: NotRequired[int]
    idrInterval: NotRequired[int]


class StreamInfo(TypedDict):
    audio: AudioStreamOptions
    video: VideoStreamOptions


class BasePrebufferState(TypedDict):
    maxDuration: int
    availableDuration: int


class PrebufferStateTrue(BasePrebufferState):
    state: bool
    url: str


class PrebufferStateFalse(BasePrebufferState):
    state: bool


PrebufferState = Union[PrebufferStateTrue, PrebufferStateFalse]

Container = Literal["mpegts", "mp4"]


class CameraDelegate(ABC):
    @abstractmethod
    async def snapshot_request(self, request_id: str) -> bytes:
        pass

    @abstractmethod
    async def prepare_stream(self, request_id: str) -> None:
        pass

    @abstractmethod
    async def on_offer(self, request_id: str, sdp: str) -> str:
        pass

    @abstractmethod
    async def on_candidates(self, request_id: str, candidates: str) -> None:
        pass

    @abstractmethod
    async def reboot(self) -> None:
        pass


class CameraPrebufferDelegate(ABC):
    @abstractmethod
    async def get_stream_info(self, source_name: str) -> Optional[StreamInfo]:
        pass


class CameraSource(Protocol):
    # from CameraInput
    id: str  # _id
    name: str
    roles: list["CameraRoles"]
    urls: StreamUrls
    # end

    async def update_prebuffering_state(self, container: Container, state: PrebufferState) -> None: ...
    def get_prebuffering_state(self, container: Container) -> PrebufferState: ...
    def on_prebuffering(self, container: Container) -> Observable[PrebufferState]: ...
    async def get_stream_info(self) -> Optional[StreamInfo]: ...


class ImageFormat(TypedDict):
    to: Literal["rgba", "gray"]


class ImageCrop(TypedDict):
    top: int
    left: int
    width: int
    height: int


class ImageResize(TypedDict):
    width: NotRequired[int]
    height: NotRequired[int]


class ImageOptions(TypedDict):
    format: NotRequired[ImageFormat]
    crop: NotRequired[ImageCrop]
    resize: NotRequired[ImageResize]


class IceServer(TypedDict):
    urls: list[str]
    username: NotRequired[str]
    credential: NotRequired[str]


class FrameMetadata(TypedDict):
    format: str
    frameSize: int
    width: int
    height: int
    origWidth: int
    origHeight: int


class ImageInformation(TypedDict):
    width: int
    height: int
    channels: int


class FrameBuffer(TypedDict):
    image: bytes
    info: ImageInformation


class FrameImage(TypedDict):
    image: Image.Image
    info: ImageInformation


class VideoFrame(Protocol):
    image_buffer: bytes

    @property
    def metadata(self) -> FrameMetadata: ...
    @property
    def input_width(self) -> int: ...
    @property
    def input_height(self) -> int: ...
    @property
    def input_format(self) -> str: ...
    async def save(self, path: str, options: Optional[ImageOptions] = None) -> None: ...
    async def to_buffer(self, options: Optional[ImageOptions] = None) -> FrameBuffer: ...
    async def to_image(self, options: Optional[ImageOptions] = None) -> FrameImage: ...


class MotionFrame(VideoFrame):
    motion: MotionState


SV = TypeVar("SV", bound=StateValue)
PV = TypeVar("PV", bound=PropertyValue)


class CameraStateChangedObject(Generic[SV], dict[str, SV]):
    old_state: SV
    new_state: SV


class CameraPropertyObservableObject(Generic[PV], dict[str, PV]):
    property: str
    old_state: PV
    new_state: PV


class CameraDevice(Protocol):
    id: str
    plugin_id: str
    native_id: Optional[str] = None
    connected: bool
    disabled: bool
    name: str
    type: CameraType
    info: CameraInformation
    sources: list[CameraSource]
    activity_zones: list[DetectionZone]
    activity_settings: CameraActivitySettings
    is_cloud: bool
    has_light: bool
    has_siren: bool
    has_binary_sensor: bool
    has_battery: bool
    has_motion_detector: bool
    has_audio_detector: bool
    has_object_detector: bool
    has_ptz: bool
    has_prebuffer: bool
    has_intercom: bool

    on_connected: Observable[bool]
    on_light_switched: Observable[LightState]
    on_motion_detected: Observable[MotionState]
    on_audio_detected: Observable[AudioState]
    on_object_detected: Observable[ObjectState]
    on_doorbell_pressed: Observable[DoorbellState]
    on_siren_detected: Observable[SirenState]
    on_battery_changed: Observable[BatteryState]

    stream_source: CameraSource
    snapshot_source: CameraSource
    recording_source: CameraSource
    detection_source: CameraSource
    delegate: Optional[CameraDelegate] = None
    prebuffer_delegate: Optional[CameraPrebufferDelegate] = None

    async def connect(self) -> None: ...
    async def disconnect(self) -> None: ...
    async def reboot(self) -> None: ...
    async def snapshot(self, force_new: Optional[bool] = None) -> bytes: ...
    async def get_frames(self) -> AsyncGenerator[VideoFrame, None]: ...
    async def get_motion_frames(self) -> AsyncGenerator[MotionFrame, None]: ...
    async def get_ffmpeg_path(self) -> str: ...
    async def get_ice_servers(self) -> list[IceServer]: ...

    async def get_value(
        self, state_name: str
    ) -> Union[
        LightState,
        MotionState,
        AudioState,
        ObjectState,
        DoorbellState,
        SirenState,
        BatteryState,
    ]: ...

    @overload
    async def update_state(
        self,
        state_name: Literal["light"],
        event_data: LightSetEvent,
    ) -> None: ...

    @overload
    async def update_state(
        self,
        state_name: Literal["motion"],
        event_data: MotionSetEvent,
        frame: Optional[bytes] = None,
    ) -> None: ...

    @overload
    async def update_state(
        self,
        state_name: Literal["audio"],
        event_data: AudioSetEvent,
    ) -> None: ...

    @overload
    async def update_state(
        self,
        state_name: Literal["object"],
        event_data: ObjectSetEvent,
    ) -> None: ...

    @overload
    async def update_state(
        self,
        state_name: Literal["doorbell"],
        event_data: DoorbellSetEvent,
    ) -> None: ...

    @overload
    async def update_state(
        self,
        state_name: Literal["siren"],
        event_data: SirenSetEvent,
    ) -> None: ...

    @overload
    async def update_state(
        self,
        state_name: Literal["battery"],
        event_data: BatterySetEvent,
    ) -> None: ...
    async def update_state(self, state_name: str, event_data: Any, frame: Optional[bytes] = None) -> None: ...

    @overload
    def on_state_change(
        self, state_name: Literal["light"]
    ) -> Observable[CameraStateChangedObject[LightState]]: ...
    @overload
    def on_state_change(
        self, state_name: Literal["motion"]
    ) -> Observable[CameraStateChangedObject[MotionState]]: ...
    @overload
    def on_state_change(
        self, state_name: Literal["audio"]
    ) -> Observable[CameraStateChangedObject[AudioState]]: ...
    @overload
    def on_state_change(
        self, state_name: Literal["doorbell"]
    ) -> Observable[CameraStateChangedObject[DoorbellState]]: ...
    @overload
    def on_state_change(
        self, state_name: Literal["siren"]
    ) -> Observable[CameraStateChangedObject[SirenState]]: ...
    @overload
    def on_state_change(
        self, state_name: Literal["battery"]
    ) -> Observable[CameraStateChangedObject[BatteryState]]: ...
    @overload
    def on_state_change(
        self, state_name: Literal["object"]
    ) -> Observable[CameraStateChangedObject[ObjectState]]: ...
    def on_state_change(  # type: ignore
        self, state_name: StateNames
    ) -> Observable[CameraStateChangedObject[StateValue]]: ...

    @overload
    def on_property_change(
        self, property_name: Literal["name"]
    ) -> Observable[CameraPropertyObservableObject[str]]: ...
    @overload
    def on_property_change(
        self,
        property_name: Literal[
            "disabled",
            "isCloud",
            "hasLight",
            "hasSiren",
            "hasBinarySensor",
            "hasBattery",
            "hasAudioDetector",
            "hasMotionDetector",
            "hasObjectDetector",
            "hasPrebuffer",
            "hasIntercom",
            "hasPtz",
        ],
    ) -> Observable[CameraPropertyObservableObject[bool]]: ...
    @overload
    def on_property_change(
        self, property_name: Literal["info"]
    ) -> Observable[CameraPropertyObservableObject[CameraInformation]]: ...
    @overload
    def on_property_change(
        self, property_name: Literal["type"]
    ) -> Observable[CameraPropertyObservableObject[CameraType]]: ...
    @overload
    def on_property_change(
        self, property_name: Literal["activityZones"]
    ) -> Observable[CameraPropertyObservableObject[list[DetectionZone]]]: ...
    @overload
    def on_property_change(
        self, property_name: Literal["activitySettings"]
    ) -> Observable[CameraPropertyObservableObject[CameraActivitySettings]]: ...
    @overload
    def on_property_change(
        self, property_name: Literal["sources"]
    ) -> Observable[CameraPropertyObservableObject[list[CameraInput]]]: ...
    def on_property_change(  # type: ignore
        self, property_name: CameraPublicProperties
    ) -> Observable[CameraPropertyObservableObject[PropertyValue]]: ...

    def remove_all_listeners(self) -> None: ...


# camera create config
class BaseCameraConfig(TypedDict):
    name: str
    nativeId: NotRequired[str]
    isCloud: NotRequired[bool]
    hasLight: NotRequired[bool]
    hasSiren: NotRequired[bool]
    hasBinarySensor: NotRequired[bool]
    hasBattery: NotRequired[bool]
    disabled: NotRequired[bool]
    info: NotRequired[CameraInformation]


class CameraInputSettings(TypedDict):
    _id: str
    name: str
    roles: list[CameraRoles]
    urls: list[str]


class CameraConfigWithSources(BaseCameraConfig):
    sources: NotRequired[list[CameraInputSettings]]


class CameraConfigWithDelegate(BaseCameraConfig):
    delegate: NotRequired[CameraDelegate]


CameraConfig = Union[CameraConfigWithSources, CameraConfigWithDelegate]


# events and callbacks
CameraSelectedCallback = Union[
    Callable[[CameraDevice, CameraExtension], None],
    Callable[[CameraDevice, CameraExtension], Coroutine[None, None, None]],
]
CameraDeselectedCallback = Union[
    Callable[[str, CameraExtension], None],
    Callable[[str, CameraExtension], Coroutine[None, None, None]],
]
CameraUpdatedCallback = Union[
    Callable[[str, CameraExtension], None],
    Callable[[str, CameraExtension], Coroutine[None, None, None]],
]


# abstract


# DeviceManager
DeviceManagerEventType = Literal[
    "cameraSelected",
    "cameraDeselected",
]


@runtime_checkable
class DeviceManager(Protocol):
    async def get_camera_by_id(self, id: str) -> Optional[CameraDevice]: ...
    async def get_camera_by_name(self, name: str) -> Optional[CameraDevice]: ...
    async def create_camera(self, config: CameraConfig) -> CameraDevice: ...
    async def remove_camera_by_id(self, id: str) -> None: ...
    async def remove_camera_by_name(self, name: str) -> None: ...

    @overload
    def on(self, event: Literal["cameraSelected"], listener: CameraSelectedCallback) -> "DeviceManager": ...
    @overload
    def on(
        self, event: Literal["cameraDeselected"], listener: CameraDeselectedCallback
    ) -> "DeviceManager": ...

    @overload
    def once(self, event: Literal["cameraSelected"], listener: CameraSelectedCallback) -> "DeviceManager": ...
    @overload
    def once(
        self, event: Literal["cameraDeselected"], listener: CameraDeselectedCallback
    ) -> "DeviceManager": ...

    @overload
    def remove_listener(
        self, event: Literal["cameraSelected"], listener: CameraSelectedCallback
    ) -> "DeviceManager": ...
    @overload
    def remove_listener(
        self, event: Literal["cameraDeselected"], listener: CameraDeselectedCallback
    ) -> "DeviceManager": ...

    def remove_all_listeners(self, event: Optional[DeviceManagerEventType] = None) -> "DeviceManager": ...


# SystemManager
@runtime_checkable
class SystemManager(Protocol):
    def on(self, event: str, listener: Callback) -> "SystemManager": ...
    def once(self, event: str, listener: Callback) -> "SystemManager": ...
    def remove_listener(self, event: str, listener: Callback) -> "SystemManager": ...
    def remove_all_listeners(self, event: str) -> "SystemManager": ...


# PluginsManager
@runtime_checkable
class PluginsManager(Protocol):  # todo: add methods
    def on(self, event: str, listener: Callback) -> "PluginsManager": ...
    def once(self, event: str, listener: Callback) -> "PluginsManager": ...
    def remove_listener(self, event: str, listener: Callback) -> "PluginsManager": ...
    def remove_all_listeners(self, event: str) -> "PluginsManager": ...


# camera storage
P = TypeVar("P")


@runtime_checkable
class CameraStorage(Protocol):
    async def initialize_storage(self) -> None: ...
    @overload
    def get_value(self, path: str) -> Union[Awaitable[P], P, None]: ...
    @overload
    def get_value(self, path: str, default_value: P) -> Union[Awaitable[P], P]: ...
    def get_value(self, path: str, default_value: Optional[P] = None) -> Union[Awaitable[P], P, None]: ...
    async def set_value(self, path: str, new_value: Any) -> None: ...
    def has_value(self, path: str) -> bool: ...
    async def getConfig(self) -> SchemaConfig: ...
    async def setConfig(self, new_config: dict[str, Any]) -> None: ...
    @overload
    async def add_schema(self, schema_or_path: PluginJsonSchemaForm) -> None: ...
    @overload
    async def add_schema(self, schema_or_path: str, schema: PluginJsonSchema) -> None: ...
    async def add_schema(
        self,
        schema_or_path: Union[PluginJsonSchemaForm, str],
        schema: Optional[PluginJsonSchema] = None,
    ) -> None: ...
    def remove_schema(self, path: str) -> None: ...
    async def change_schema(self, path: str, new_schema: dict[str, Any]) -> None: ...
    def get_schema(self, path: str) -> Optional[PluginJsonSchema]: ...
    def has_schema(self, path: str) -> bool: ...


# StorageController
@runtime_checkable
class StorageController(Protocol):
    def create_camera_storage(
        self,
        instance: Any,
        camera_id: str,
        schema: Optional[PluginJsonSchemaForm] = None,
    ) -> CameraStorage: ...
    def get_camera_storage(self, camera_id: str) -> Optional[CameraStorage]: ...
    def remove_camera_storage(self, camera_id: str) -> None: ...


# config service
@runtime_checkable
class PluginConfigService(Protocol):
    def get(
        self,
        key: str,
        default: Optional[Any] = None,
        validate: Optional[Callable[[Any], bool]] = None,
        refresh: bool = False,
        write_if_not_valid: bool = False,
    ) -> Any: ...

    def has(self, key: str, refresh: bool = False) -> bool: ...
    def ensure_exists(self, key: str, default: Optional[Any] = None, write: bool = False) -> None: ...
    def set(self, key: str, value: Any, write: bool = False) -> None: ...
    def insert(self, key: str, value: Any, index: Optional[int] = None, write: bool = False) -> None: ...
    def push(self, key: str, *values: Any, write: bool = False) -> None: ...
    def delete(self, key: str, write: bool = False) -> None: ...
    def all(self, refresh: bool = False) -> dict[str, Any]: ...
    def replace(self, new_config: dict[str, Any], write: bool = False) -> None: ...
    def update_value(
        self,
        path: str,
        search_key: str,
        search_value: Any,
        target_key: str,
        new_value: Any,
        write: bool = False,
    ) -> None: ...
    def replace_or_add_item(
        self,
        path: str,
        search_key: str,
        search_value: Any,
        new_item: Any,
        write: bool = False,
    ) -> None: ...


# Plugin API
APIEventType = Literal["finishLaunching", "shutdown"]


@runtime_checkable
class PluginAPI(Protocol):
    storage_path: str
    config_file: str
    config_service: PluginConfigService
    storage_controller: StorageController
    device_manager: DeviceManager
    system_manager: SystemManager
    plugins_manager: PluginsManager

    def on(self, event: APIEventType, listener: Callback) -> "PluginAPI": ...
    def once(self, event: APIEventType, listener: Callback) -> "PluginAPI": ...
    def off(self, event: APIEventType, listener: Callback) -> "PluginAPI": ...
    def remove_listener(self, event: APIEventType, listener: Callback) -> "PluginAPI": ...
    def remove_all_listeners(self, event: Optional[APIEventType] = None) -> "PluginAPI": ...


# logger
@runtime_checkable
class PluginLogger(Protocol):
    def log(self, *args: Any) -> None: ...
    def error(self, *args: Any) -> None: ...
    def warn(self, *args: Any) -> None: ...
    def attention(self, *args: Any) -> None: ...
    def debug(self, *args: Any) -> None: ...
    def trace(self, *args: Any) -> None: ...


# plugin
PluginConfig = dict[str, Any]
JSONValue = Union[str, int, float, bool, dict[str, Any], list[Any]]


class BasePlugin(ABC):
    @abstractmethod
    def __init__(self, logger: PluginLogger, api_instance: PluginAPI) -> None: ...
    @abstractmethod
    async def onFormSubmit(self, action_id: str, payload: Any) -> dict[Literal["toastMessage"], str]: ...
    @abstractmethod
    def configure_cameras(self, cameras: list[CameraDevice]) -> None: ...
