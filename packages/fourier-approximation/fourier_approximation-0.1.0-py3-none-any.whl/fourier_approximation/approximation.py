import numpy as np

def approximate_fourier(signal, num_terms):
    """
    Approximates the Fourier series of a given signal using a specified number of terms.
    
    Parameters:
    - signal: The input signal (assumed to be periodic).
    - num_terms: The number of Fourier terms to use for the approximation.
    
    Returns:
    - approx_signal: The approximated signal using the Fourier series.
    """
    N = len(signal)
    approx_signal = np.zeros(N, dtype=complex)
    t = np.arange(N)

    for k in range(num_terms):
        # Calculate the Fourier coefficients
        c_k = (1/N) * np.sum(signal * np.exp(-2j * np.pi * k * t / N))
        # Add the k-th term of the Fourier series
        approx_signal += c_k * np.exp(2j * np.pi * k * t / N)

    return approx_signal.real  # Return the real part of the signal
