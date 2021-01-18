import wgpu
import math
import wgpu.backends.rs  # Select backend
from wgpu.utils import compute_with_buffers  # Convenience function
from pyshader import python2shader, ivec3, i32, Array, vec3, f32, vec4, ivec4

@python2shader
def compute_shader(
    index: ("input", "GlobalInvocationId", ivec3),
    image: ("buffer", 0, Array(vec4)),
    output: ("buffer", 1, Array(vec4)),
    lut: ("buffer", 2, Array(vec4)),
    size: ("uniform", 3, i32),
):
    i = index.x
    coords = ivec4(math.floor(image[i] * f32(size - 1)))
    output[i] = clamp(lut[coords.r * size ** 2 + coords.g * size + coords.b], 0., 1.)

