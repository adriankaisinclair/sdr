# 21 cm astro 
# 1, 420, 405, 751.7667±0.0009 Hz from wiki
from pylab import *
from rtlsdr import *

sdr = RtlSdr()

# configure device
sdr.sample_rate = 2.4e6
sdr.center_freq = 1419.405752e6 # MHz, shifted by 1MHz to avoid LO leakage
sdr.gain = 496

plt.ion()

def get_samples():
  samples = sdr.read_samples(256*1024)
  #sdr.close()
  return samples

def plot_psd(color="blue",label="on"):
  # use matplotlib to estimate and plot the PSD
  plt.ion()
  samps = get_samples()
  psd(samps, NFFT=1024, Fs=sdr.sample_rate/1e6, Fc=sdr.center_freq/1e6)
  xlabel('Frequency (MHz)')
  ylabel('Relative power (dB)')
  show()
  return

def live_spectrum(avg=False):
  plt.ion()
  freqs = np.fft.fftfreq(1024,d=1./sdr.sample_rate)
  samps = get_samples()
  X = np.fft.fft(samps,n=1024,norm="ortho")
  plt.plot(freqs/1e6,np.abs(X)**2)
  plt.ylim(0,1000.0)
  plt.show()
  for i in range(1000):
    plt.clf()
    samps = get_samples()
    X = np.fft.fft(samps,n=1024,norm="ortho")
    Xacc = 0
    if avg==True:
      Xacc += X
      plt.plot(freqs/1e6,np.abs(Xacc)**2/i)
      plt.title("Avg # "+str(i))
    else:
      plt.plot(freqs/1e6,np.abs(X)**2)
    #psd(samps, NFFT=1024, Fs=sdr.sample_rate/1e6, Fc=sdr.center_freq/1e6)
    plt.ylim(0,1000.0)
    xlabel('Frequency (MHz)')
    ylabel('Relative power')
    plt.pause(0.001)
  plt.show()
  return
      
def live_timestream():
  plt.ion()
  samps = get_samples()
  plt.plot(samps)
  plt.ylim(-1,1)
  plt.xlim(0,len(samps))
  plt.show()
  for i in range(1000):
    samps = get_samples()
    plt.plot(samps)
    plt.pause(0.1)
  plt.show()
  return

print("Running..")
