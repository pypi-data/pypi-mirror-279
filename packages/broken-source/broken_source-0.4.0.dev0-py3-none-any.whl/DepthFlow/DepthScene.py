import math
from typing import Annotated, Iterable, Tuple

import imgui
from attr import define, field
from pydantic import BaseModel, Field
from ShaderFlow.Message import ShaderMessage
from ShaderFlow.Modules.Depth import (
    DepthAnything,
    DepthAnythingV2,
    DepthEstimator,
    Marigold,
    ZoeDepth,
)
from ShaderFlow.Scene import ShaderScene
from ShaderFlow.Texture import ShaderTexture
from ShaderFlow.Variable import ShaderVariable
from typer import Option

from Broken import image_hash
from Broken.Externals.Upscaler import BrokenUpscaler, RealEsrgan
from Broken.Loaders import LoaderImage
from DepthFlow import DEPTHFLOW


class DepthFlowState(BaseModel):

    height: float = Field(default=0.35)
    """Peak value of the Depth Map, in the range [0, 1]. The camera is 1 distance away from depth=0
    at the z=1 plane, so this also controls the intensity of the effect"""

    static: float = Field(default=0.25)
    """Focal depth of offsets, in the range [0, 1]. A value of 0 makes the background (depth=0)
    stationary, while a value of 1 makes the foreground (depth=1) stationary on offset changes"""

    focus: float = Field(default=0.5)
    """Focal depth of projections, in the range [0, 1]. A value of 0 makes the background (depth=0)
    stationaty, while a value of 1 makes the foreground (depth=1) stationary on isometric changes"""

    invert: float = Field(default=0.0)
    """Interpolate between (0=max, 1=min)=0 or (0=min, 1=max)=1 Depth Map's value interpretation"""

    zoom: float = Field(default=0.88)
    """Camera zoom factor, in the range [0, inf]. 2 means a quarter of the image is visible"""

    isometric: float = Field(default=0.0)
    """Isometric factor of the camera projection. Zero is fully perspective, 1 is orthographic"""

    dolly: float = Field(default=0.0)
    """Same effect as isometric, but with "natural units" of AFAIK `isometric = atan(dolly)*(2/pi)`.
    Keeps the ray target constant and move back ray origins by this amount"""

    mirror: bool = Field(default=True)
    """Apply GL_MIRRORED_REPEAT to the image, makes it continuous"""

    # # Center

    center_x: float = Field(default=0)
    """Horizontal 'true' offset of the camera, the camea *is* above this point"""

    center_y: float = Field(default=0)
    """Vertical 'true' offset of the camera, the camea *is* above this point"""

    @property
    def center(self) -> Tuple[float, float]:
        """'True' offset of the camera, the camea *is* above this point"""
        return (self.center_x, self.center_y)

    @center.setter
    def center(self, value: Tuple[float, float]):
        self.center_x, self.center_y = value

    # # Origin

    origin_x: float = Field(default=0)
    """Hozirontal focal point of the offsets, *as if* the camera was above this point"""

    origin_y: float = Field(default=0)
    """Vertical focal point of the offsets, *as if* the camera was above this point"""

    @property
    def origin(self) -> Tuple[float, float]:
        """Focal point of the offsets, *as if* the camera was above this point"""
        return (self.origin_x, self.origin_y)

    @origin.setter
    def origin(self, value: Tuple[float, float]):
        self.origin_x, self.origin_y = value

    # # Parallax

    offset_x: float = Field(default=0)
    """Parallax horizontal displacement, change this over time for the 3D effect"""

    offset_y: float = Field(default=0)
    """Parallax vertical displacement, change this over time for the 3D effect"""

    @property
    def offset(self) -> Tuple[float, float]:
        """Parallax displacement, change this over time for the 3D effect"""
        return (self.offset_x, self.offset_y)

    @offset.setter
    def offset(self, value: Tuple[float, float]):
        self.offset_x, self.offset_y = value

    # # Special

    def reset(self) -> None:
        for name, field in self.model_fields.items(): # noqa
            setattr(self, name, field.default)

    class _PFX_DOF(BaseModel):
        enable:     bool  = Field(default=False)
        start:      float = Field(default=0.6)
        end:        float = Field(default=1.0)
        exponent:   float = Field(default=2.0)
        intensity:  float = Field(default=1)
        quality:    int   = Field(default=4)
        directions: int   = Field(default=16)

        def pipeline(self) -> Iterable[ShaderVariable]:
            yield ShaderVariable("uniform", "bool",  "iDofEnable",     self.enable)
            yield ShaderVariable("uniform", "float", "iDofStart",      self.start)
            yield ShaderVariable("uniform", "float", "iDofEnd",        self.end)
            yield ShaderVariable("uniform", "float", "iDofExponent",   self.exponent)
            yield ShaderVariable("uniform", "float", "iDofIntensity",  self.intensity/100)
            yield ShaderVariable("uniform", "int",   "iDofQuality",    self.quality)
            yield ShaderVariable("uniform", "int",   "iDofDirections", self.directions)

    dof: _PFX_DOF = Field(default_factory=_PFX_DOF)
    """Depth of Field Post-Processing configuration"""

    class _PFX_Vignette(BaseModel):
        enable:    bool  = Field(default=False)
        intensity: float = Field(default=30)
        decay:     float = Field(default=0.1)

        def pipeline(self) -> Iterable[ShaderVariable]:
            yield ShaderVariable("uniform", "bool",  "iVignetteEnable",    self.enable)
            yield ShaderVariable("uniform", "float", "iVignetteIntensity", self.intensity)
            yield ShaderVariable("uniform", "float", "iVignetteDecay",     self.decay)

    vignette: _PFX_Vignette = Field(default_factory=_PFX_Vignette)
    """Vignette Post-Processing configuration"""

    def pipeline(self) -> Iterable[ShaderVariable]:
        yield ShaderVariable("uniform", "float", "iDepthHeight",    self.height)
        yield ShaderVariable("uniform", "float", "iDepthStatic",    self.static)
        yield ShaderVariable("uniform", "float", "iDepthFocus",     self.focus)
        yield ShaderVariable("uniform", "float", "iDepthInvert",    self.invert)
        yield ShaderVariable("uniform", "float", "iDepthZoom",      self.zoom)
        yield ShaderVariable("uniform", "float", "iDepthIsometric", self.isometric)
        yield ShaderVariable("uniform", "float", "iDepthDolly",     self.dolly)
        yield ShaderVariable("uniform", "vec2",  "iDepthCenter",    self.center)
        yield ShaderVariable("uniform", "vec2",  "iDepthOrigin",    self.origin)
        yield ShaderVariable("uniform", "vec2",  "iDepthOffset",    self.offset)
        yield ShaderVariable("uniform", "bool",  "iDepthMirror",    self.mirror)
        yield from self.dof.pipeline()
        yield from self.vignette.pipeline()

# -------------------------------------------------------------------------------------------------|

@define
class DepthFlowScene(ShaderScene):
    """🌊 Image to → 2.5D Parallax Effect Video. High quality, user first"""
    __name__ = "DepthFlow"

    # Constants
    DEFAULT_IMAGE = "https://w.wallhaven.cc/full/pk/wallhaven-pkz5r9.png"
    DEPTH_SHADER  = (DEPTHFLOW.RESOURCES.SHADERS/"DepthFlow.glsl")

    # DepthFlow objects
    estimator: DepthEstimator = field(factory=DepthAnything)
    upscaler: BrokenUpscaler = field(factory=RealEsrgan)
    state: DepthFlowState = field(factory=DepthFlowState)

    def input(self,
        image:   Annotated[str,  Option("--image",   "-i", help="• Image to Parallax (Path, URL, NumPy, PIL)")],
        depth:   Annotated[str,  Option("--depth",   "-d", help="• Depthmap of the Image, None to estimate")]=None,
        cache:   Annotated[bool, Option(" /--nc",          help="• Cache the Depthmap estimations on Disk")]=True,
        upscale: Annotated[int,  Option("--upscale", "-u", help="• Upscale the Input image by a ratio (1, 2, 3, 4)")]=1,
    ) -> None:
        """Load an Image from Path, URL and its estimated DepthMap to the Scene, and optionally upscale it. See 'input --help'"""
        image = LoaderImage(image)
        depth = LoaderImage(depth) or self.estimator.estimate(image, cache=cache)
        width, height = image.size
        cache = DEPTHFLOW.DIRECTORIES.CACHE/f"{image_hash(image)}"
        image = self.upscaler.upscale(image, scale=upscale)
        self.aspect_ratio = (width/height)
        self.image.from_image(image)
        self.depth.from_image(depth)
        self.time = 0

    def commands(self):
        self.typer.command(self.input)

    def setup(self):
        if self.image.is_empty():
            self.input(image=DepthFlowScene.DEFAULT_IMAGE)

    def build(self):
        ShaderScene.build(self)
        self.image = ShaderTexture(scene=self, name="image").repeat(False)
        self.depth = ShaderTexture(scene=self, name="depth").repeat(False)
        self.shader.fragment = self.DEPTH_SHADER
        self.aspect_ratio = (16/9)

    def update(self):

        # In and out dolly zoom
        self.state.dolly = (0.5 + 0.5*math.cos(self.cycle))

        # Infinite 8 loop shift
        self.state.offset_x = (0.2 * math.sin(1*self.cycle))
        self.state.offset_y = (0.2 * math.sin(2*self.cycle))

        # Oscillating rotation
        self.camera.rotate(
            direction=self.camera.base_z,
            angle=math.cos(self.cycle)*self.dt*0.4
        )

        # Zoom in on the start
        # self.config.zoom = 1.2 - 0.2*(2/math.pi)*math.atan(self.time)

    def handle(self, message: ShaderMessage):
        ShaderScene.handle(self, message)

        if isinstance(message, ShaderMessage.Window.FileDrop):
            files = iter(message.files)
            self.input(image=next(files), depth=next(files, None))

    def pipeline(self) -> Iterable[ShaderVariable]:
        yield from ShaderScene.pipeline(self)
        yield from self.state.pipeline()

    def ui(self) -> None:
        if (state := imgui.slider_float("Height", self.state.height, 0, 1, "%.2f"))[0]:
            self.state.height = max(0, state[1])
        if (state := imgui.slider_float("Static", self.state.static, 0, 1, "%.2f"))[0]:
            self.state.static = max(0, state[1])
        if (state := imgui.slider_float("Focus", self.state.focus, 0, 1, "%.2f"))[0]:
            self.state.focus = max(0, state[1])
        if (state := imgui.slider_float("Invert", self.state.invert, 0, 1, "%.2f"))[0]:
            self.state.invert = max(0, state[1])
        if (state := imgui.slider_float("Zoom", self.state.zoom, 0, 2, "%.2f"))[0]:
            self.state.zoom = max(0, state[1])
        if (state := imgui.slider_float("Isometric", self.state.isometric, 0, 1, "%.2f"))[0]:
            self.state.isometric = max(0, state[1])
        if (state := imgui.slider_float("Dolly", self.state.dolly, 0, 5, "%.2f"))[0]:
            self.state.dolly = max(0, state[1])

        imgui.text("- True camera position")
        if (state := imgui.slider_float("Center X", self.state.center_x, -self.aspect_ratio, self.aspect_ratio, "%.2f"))[0]:
            self.state.center_x = state[1]
        if (state := imgui.slider_float("Center Y", self.state.center_y, -1, 1, "%.2f"))[0]:
            self.state.center_y = state[1]

        imgui.text("- Fixed point at height changes")
        if (state := imgui.slider_float("Origin X", self.state.origin_x, -self.aspect_ratio, self.aspect_ratio, "%.2f"))[0]:
            self.state.origin_x = state[1]
        if (state := imgui.slider_float("Origin Y", self.state.origin_y, -1, 1, "%.2f"))[0]:
            self.state.origin_y = state[1]

        imgui.text("- Parallax offset")
        if (state := imgui.slider_float("Offset X", self.state.offset_x, -2, 2, "%.2f"))[0]:
            self.state.offset_x = state[1]
        if (state := imgui.slider_float("Offset Y", self.state.offset_y, -2, 2, "%.2f"))[0]:
            self.state.offset_y = state[1]
