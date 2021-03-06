import matplotlib.pyplot as plt
import math
from random import *
import numpy as np
import timeit, time


n = 12
N = 64
omega = 1100

def generateFreq(omega, n):
    freq = []
    step = omega / n
    for i in range(n):
        freq.append(omega - step * i)
    return freq


def generateXt(N, n, A, freq, alpha):
    x = [0] * N
    for j in range(N):
        for i in range(n):
            x[j] += A[i] * math.sin(freq[i] * j + alpha[i])
    return x


def mathExpecation(x, N):
    mx = 0.0
    for i in range(N):
        mx += x[i]
    return mx / N


def dispersion(x, N, mx):
    dx = 0.0
    for i in range(N):
        dx += math.pow(x[i] - mx, 2)
    return dx / (N - 1)


def arrGenerator(n, min, max):
    arr = [0] * n
    for i in range(n):
        arr[i] = randint(min, max)
    return arr

def dpf(signal):
    n = len(signal)
    p = np.arange(n)
    k = p.reshape((n, 1))
    w = np.exp(-2j * np.pi * p * k / n)
    return np.dot(w, signal)

def fft(signal):
    signal = np.asanyarray(signal, dtype=float)
    N = len(signal)
    if N <= 2:
        return dpf(signal)
    else:
        signal_even = fft(signal[::2])
        signal_odd = fft(signal[1::2])
        terms = np.exp(-2j * np.pi * np.arange(N) / N)
        return np.concatenate([signal_even + terms[:N // 2] * signal_odd,
                               signal_even + terms[N // 2:] * signal_odd])


A = arrGenerator(n, 0, 5)
alpha  = arrGenerator(n, 0, 5)
freq = generateFreq(omega, n)
x = generateXt(N, n, A, freq, alpha)
x_dpf = dpf(x)
x_fft = fft(x)

t = np.linspace(0, 10, 64)
x_dpf_real = x_dpf.real
x_dpf_img = x_dpf.imag
x_fft_real = x_fft.real
x_fft_img = x_fft.imag


# Calc Task
arr_x = []
arr_dpf = []
arr_fft = []
arr_time = []

for i in range(10):
    start_dpf = time.time()
    dpf(generateXt(2**i, n, alpha, freq, alpha))
    end_dpf = time.time()
    elapsed_dpf = end_dpf-start_dpf

    start_fft = time.time()
    fft(generateXt(2**i, n, alpha, freq, alpha))
    end_fft = time.time()
    elapsed_fft = end_fft-start_fft

    arr_time.append(elapsed_fft/elapsed_dpf)

print(arr_time)

# Graphics

def draw_DPF():
    plt.title("DPF")
    plt.plot(t, x_dpf_real, 'b', t, x_dpf_img, 'r')
    plt.show()

def draw_FFT():
    plt.title("FFT")
    plt.plot(t, x_fft_real, 'b', t, x_fft_img, 'r')
    plt.show()


def draw_task(arr_time):
    plt.title("T(FFT)/T(DPF)")
    N = []
    for i in range(10):
        N.append( 2**i )

    plt.plot(N, arr_time, label="task")

    plt.show()



draw_DPF()
draw_FFT()
draw_task(arr_time)
