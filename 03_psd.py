import mne
import numpy as np
import matplotlib.pyplot as plt
psd_file=r"C:\Lab\neurodata\physionet-sleep-data\SC4001E0-PSG.edf"
#周波数のフィルタリング
L_FREQ=0.5
H_FREQ=40.0
raw=mne.io.read_raw_edf(psd_file,preload=True)
raw_filtered=raw.copy().filter(l_freq=L_FREQ,h_freq=H_FREQ)
#全体PSDの表示
FMIN=0.5
FMAX=40.0
PICKS='eeg'
specrtrum=raw_filtered.compute_psd(method='welch', fmin=FMIN, fmax=FMAX,picks=PICKS)
specrtrum.plot()
plt.show()
#epochs化
annotations=mne.read_annotations(r"C:\Lab\neurodata\physionet-sleep-data\SC4001EC-Hypnogram.edf")
raw_filtered.set_annotations(annotations)
annotation_desc_to_event_id={
    'Sleep stage W':0,
    'Sleep stage 1':1,
    'Sleep stage 2':2,
    'Sleep stage 3':3,
    'Sleep stage 4':4,
    'Sleep stage R':5}
events,event_id=mne.events_from_annotations(
    raw_filtered,
    event_id=annotation_desc_to_event_id,
    chunk_duration=30.0)
print(events.shape)
print(event_id)
print(events[:5])
#epochsの作成
TMAX=30.0-1.0/raw_filtered.info['sfreq']
epochs=mne.Epochs(raw_filtered,events,event_id=event_id,tmin=0.0,tmax=TMAX,baseline=None,preload=True)
print(epochs)
#睡眠ステージごとのPSDの表示
epochs_rem=epochs['Sleep stage R']
epochs_n3=epochs['Sleep stage 3','Sleep stage 4']
psd_rem=epochs_rem.compute_psd(method='welch',fmin=FMIN,fmax=FMAX)
psd_n3=epochs_n3.compute_psd(method='welch',fmin=FMIN,fmax=FMAX)
psd_rem.plot(show=False)
plt.title('REM sleep')
plt.show()
psd_n3.plot(show=False)
plt.title('N3 sleep')
plt.show()