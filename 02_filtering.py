import mne
import matplotlib.pyplot as plt
psg_file= r"C:\Lab\neurodata\physionet-sleep-data\SC4001E0-PSG.edf"
raw=mne.io.read_raw_edf(psg_file,preload=True)
print(raw.info)

L_FREQ=0.5
H_FREQ=40.0
raw_filtered=raw.copy().filter(l_freq=L_FREQ,h_freq=H_FREQ)
print(raw_filtered.info)

fig,axes=plt.subplots(2,1,figsize=(15,6))
DURATION=5
N_CHANNELS=2
raw.plot(duration=DURATION,n_channels=N_CHANNELS,title='Before filtering',start=0)
raw_filtered.plot(duration=DURATION,n_channels=N_CHANNELS,title='After filtering',start=0)
plt.show()

FREQS=50
raw_notch=raw_filtered.copy().notch_filter(freqs=FREQS)
print(raw_notch.info)