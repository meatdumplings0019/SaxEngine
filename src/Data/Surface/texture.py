from src.Blend import Blend
from src.Data.Resources.texture import close_resources
from src.Surface import SurfaceRender

close_surface = SurfaceRender(close_resources.res)

red_close_surface = SurfaceRender(Blend.multiply(close_resources.res, "red"))
