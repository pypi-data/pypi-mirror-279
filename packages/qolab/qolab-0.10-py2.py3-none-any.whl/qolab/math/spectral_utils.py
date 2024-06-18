import numpy as np
from scipy.fft import fft, rfft, irfft, rfftfreq

def spectrum(t, y):
    """
    Spectrum of real value signal with stripped away zero frequency component.
    Preserves amplitude of a coherent signal (Asin(f*t)) independent of sampling
    rate and time interval.
    """
    N = t.size
    dt=np.mean(np.diff(t))
    freq=rfftfreq(N, dt)
    # y= y - np.mean(y)
    yf = rfft(y)
    yf *= 2/N; # produce normalized amplitudes
    return freq[1:], yf[1:]; # strip of boring freq=0

def noise_density_spectrum(t,y):
    """
    Calculates noise amplitude spectral density (ASD), the end results has unitis of y/sqrt(Hz)
    i.e. it does sqrt(PSD) where PSD is powerd spectrum density.
    Preserves the density independent of sampling rate and time interval.
    """
    freq, yf = spectrum(t, y)
    yf = yf*np.sqrt(t[-1]-t[0]) # scales with 1/sqrt(RBW)
    return freq, yf

def noise_spectrum_smooth(fr, Ampl, Nbins=100):
    """
    Smooth spectrum, especially at high frequency end.
    Could be thought as logarithmic spacing running average.
    Since we assume the spectrum of the nose, we do power average (rmsq on amplitudes)
    Assumes that set of frequencies is positive and equidistant set.
    Also assumes that frequencies do not contain 0.
    """

    frEdges = np.logspace(np.log10(fr[0]), np.log10(fr[-1]), Nbins)
    frCenter = np.zeros(frEdges.size-1)
    power = np.zeros(frEdges.size-1)
    for i, (frStart, frEnd) in enumerate(zip(frEdges[0:-1], frEdges[1:])):
        # print (f"{i=} {frStart=} {frEnd}")
        ind = (frStart <= fr) & (fr <= frEnd)
        frCenter[i] = np.mean( fr[ind] ) 
        power [i] = np.mean( np.power( np.abs(Ampl[ind]),2) )
    ind = np.logical_not(np.isnan(frCenter))
    frCenter = frCenter[ind]
    power = power[ind]
    # print(f'{frCenter=} {power=}')
    return frCenter,  np.sqrt( power )

