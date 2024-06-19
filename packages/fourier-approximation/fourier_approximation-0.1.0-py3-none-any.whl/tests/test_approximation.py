import unittest
import numpy as np
from fourier_approximation import approximate_fourier

class TestFourierApproximation(unittest.TestCase):

    def test_sine_wave(self):
        # Create a sine wave
        t = np.linspace(0, 2 * np.pi, 1000)
        signal = np.sin(t)

        # Approximate the Fourier series with 10 terms
        approx_signal = approximate_fourier(signal, 10)

        # The approximation should be close to the original signal
        np.testing.assert_allclose(signal, approx_signal, atol=0.1)

if __name__ == '__main__':
    unittest.main()
