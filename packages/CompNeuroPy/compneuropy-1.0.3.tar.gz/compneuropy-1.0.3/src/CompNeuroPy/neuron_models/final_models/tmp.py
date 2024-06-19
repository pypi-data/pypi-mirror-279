import numpy as np
from CompNeuroPy import sci

### create an array with normal distributed ranodm numbers
np.random.seed(0)
std = 5
x = np.random.normal(0, std, 1000)

### calculate the mean of the squared values
power_noise = np.mean(x**2)
power_signal = 5

snr = power_signal / power_noise
print(f"power noise: {sci(power_noise)}")
print(f"std**2 = {sci(std**2)}")
print(f"SNR: {sci(snr)}")

target_snr = 10

### calculate the scaling factor
scaling_factor = np.sqrt(power_signal / (power_noise * 10 ** (target_snr / 10)))
print(scaling_factor)
scaling_factor = np.sqrt((power_signal / power_noise) / target_snr)
print(scaling_factor)

### scale the noise
x_scaled = np.random.normal(0, scaling_factor * std, 1000)

### calculate the new power of the noise
power_noise_scaled = np.mean(x_scaled**2)

### calculate the new SNR
snr = power_signal / power_noise_scaled
print(f"SNR: {snr}")
