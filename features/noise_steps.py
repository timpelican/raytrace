from aloe import world, step
from Noise import Noise


@step(r'[^a-z0-9\.]([A-Za-z][A-Za-z0-9_]*) <- noise\(\)')
def _noise(self, name):
    n = Noise()
    setattr(world, name, n)


@step(r'[^a-z0-9\.]([A-Za-z][A-Za-z0-9_]*)\.noise_at\(([-+]?\d*\.?\d+)\s*,'
      r'\s*([-+]?\d*\.?\d+)\)\s*=\s*([-+]?\d*\.?\d+)')
def _noise_at(self, name, x, y, value):
    n = getattr(world, name)
    nx = float(x)
    ny = float(y)
    noise = float(value)
    test_noise = n.eval2d(nx, ny)
    print("\nExpected:")
    print(noise)
    print("\nGot:")
    print(test_noise)
    assert noise == test_noise
