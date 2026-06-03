import mne
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

psg_file=r"C:\Lab\neurodata\physionet-sleep-data\SC4001E0-PSG.edf"
hypno_file=r"C:\Lab\neurodata\physionet-sleep-data\SC4001EC-Hypnogram.edf"

raw = mne.io.read_raw_edf(psg_file, preload=True)
raw_filtered=raw.copy().filter(l_freq=0.5,h_freq=40.0)

annotations=mne.read_annotations(hypno_file)
raw_filtered.set_annotations(annotations)

annotation_desc_2_event_id={
    'Sleep stage W': 0,
    'Sleep stage 1': 1,
    'Sleep stage 2': 2,
    'Sleep stage 3': 3,
    'Sleep stage 4': 4,
    'Sleep stage R': 5
}
events,event_id=mne.events_from_annotations(raw_filtered, event_id=annotation_desc_2_event_id,chunk_duration=30.0)
tmax=30.0-1.0/raw_filtered.info['sfreq']
epochs=mne.Epochs(raw_filtered,events,event_id=event_id,tmin=0.0,tmax=tmax,baseline=None,preload=True)

epochs_rem=epochs['Sleep stage R']
epochs_n3=epochs['Sleep stage 3','Sleep stage 4']

psd_rem=epochs_rem.compute_psd(method='welch',fmin=0.5,fmax=40.0)
psd_n3=epochs_n3.compute_psd(method='welch',fmin=0.5,fmax=40.0)

freqs=psd_rem.freqs
delta_mask=(freqs>=0.5)&(freqs<=4.0)

power_rem=psd_rem.get_data()[:,:,delta_mask].mean(axis=2)
power_n3=psd_n3.get_data()[:,:,delta_mask].mean(axis=2)
print(power_rem.shape)
print(power_n3.shape)

#以下からは統計解析のコード
t_stat,p_value=stats.ttest_ind(
    power_rem.mean(axis=1),
    power_n3.mean(axis=1)
)
print(f"T-statistic: {t_stat:.4f}")
print(f"p-value: {p_value:.4f}")

bands={
    'delta':(0.5,4.0),
    'theta':(4.0,8.0), 
    'alpha':(8.0,13.0),
    'beta':(13.0,30.0),
    'gamma':(30.0,40.0)
}

p_values=[]
t_values=[]

for band_name,(fmin,fmax) in bands.items():
    mask=(freqs>=fmin)&(freqs<=fmax)
    pow_rem=psd_rem.get_data()[:,:,mask].mean(axis=(1,2))
    pow_n3=psd_n3.get_data()[:,:,mask].mean(axis=(1,2))
    t,p=stats.ttest_ind(pow_rem,pow_n3)
    t_values.append(t)
    p_values.append(p)
    print(f"{band_name} band: T={t:.4f}, p={p:.4f}")

from statsmodels.stats.multitest import multipletests
reject,p_corrected,_,_=multipletests(p_values,method='fdr_bh')
for i,band_name in enumerate(bands.keys()):
    print(f"{band_name} :p-value={p_values[i]:.4f}, p-corrected={p_corrected[i]:.4f}, reject null={reject[i]}")

x=range(len(bands))
colors=['green' if r else 'red' for r in reject]
plt.bar(x,[-t for t in t_values], color=colors)
plt.xticks(x,bands.keys())
plt.ylabel('T-statistic')
plt.title('T-statistics for Power Differences Between REM and N3 Sleep')
plt.show()