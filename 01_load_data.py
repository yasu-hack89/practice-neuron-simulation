import mne
import matplotlib.pyplot as plt

#temazepam data
psg_file = r"C:\Lab\neurodata\physionet-sleep-data\SC4001E0-PSG.edf"
hypno_file= r"C:\Lab\neurodata\physionet-sleep-data\SC4001EC-Hypnogram.edf"

raw_data=mne.io.read_raw_edf(psg_file,preload=True)
print(raw_data.info)

print(raw_data.ch_names)
print(raw_data.times[-1])

print(f"Time：{raw_data.times[-1] / 3600:.2f} hours")
print(f"sample count：{len(raw_data.times)}")

raw_data.plot(duration=30,n_channels=7,scalings='auto',title='Raw Data')
plt.show()

annotations=mne.read_annotations(hypno_file)
print(annotations)

import pandas as pd

df=pd.DataFrame({
    'onset': annotations.onset,
    'duration': annotations.duration,
    'description': annotations.description
})
print(df['description'].value_counts())