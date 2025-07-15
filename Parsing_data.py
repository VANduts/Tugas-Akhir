import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

file = 'ADAPTIF_290625.TXT'

headers = [
    'waktu', 'save_pH', 'value_pH', 'interval_pH', 
    'save_temp', 'value_temp', 'interval_temp', 
    'save_DO', 'value_DO', 'interval_DO', 
    'save_turb', 'value_turb', 'interval_turb', 
    'current', 'voltage'
]

try:
    df = pd.read_csv(file, sep=';', header=None, names=headers)
    print("Parsing Berhasil!")

    hasil_akhir = {}
    sensors = ['pH', 'temp', 'DO', 'turb']

    for sensor in sensors:
        save_col = f'save_{sensor}'
        value_col = f'value_{sensor}'
        interval_col = f'interval_{sensor}'

        # Filter baris save == 1
        filtered = df[df[save_col] == 1][['waktu', value_col, interval_col]].copy()

        # Hapus duplikasi waktu
        deduplicated = filtered.drop_duplicates(subset=['waktu'], keep='first')

        # Simpan DataFrame ke dictionary
        hasil_akhir[sensor] = deduplicated
        
        print(f"Pemrosesan untuk sensor '{sensor}' selesai. Ditemukan {len(deduplicated)} baris.")

        print("\n================ HASIL AKHIR ==================\n")
    for sensor, data in hasil_akhir.items():
        print(f"--- Data untuk Sensor: {sensor} ---")
        print("\n")

    fig, axes = plt.subplots(4, 2, figsize=(20, 25), sharex=True)
    fig.suptitle('Grafik Nilai & Interval Sensor Terhadap Waktu Adaptive', fontsize=18)

    for i, sensor in enumerate(sensors):
        ax1 = axes[i, 0] 
        ax2 = axes[i, 1] 
        
        data = hasil_akhir[sensor]
        
        if not data.empty:
            data['datetime'] = pd.to_datetime(data['waktu'], format='%H:%M:%S:%f')
            data = data.sort_values('datetime')
            
            value_col = f'value_{sensor}'
            interval_col = f'interval_{sensor}'
            
            # Plot NILAI di kolom kiri
            ax1.plot(data['datetime'], data[value_col], marker='o', linestyle='-', markersize=4, color='royalblue')
            ax1.set_title(f'Nilai Sensor {sensor.upper()}', fontsize=14)
            ax1.grid(True, linestyle='--', alpha=0.6)

            # Plot INTERVAL di kolom kanan
            ax2.plot(data['datetime'], data[interval_col], marker='x', linestyle='--', markersize=4, color='green')
            ax2.set_title(f'Interval Sensor {sensor.upper()}', fontsize=14)
            ax2.set_ylabel('Interval (ms)')
            ax2.grid(True, linestyle='--', alpha=0.6)

            # Atur label Y sesuai dengan satuan setelah kalibrasi
            if sensor == 'pH':
                ax1.set_ylabel('pH')
            elif sensor == 'temp':
                ax1.set_ylabel('Suhu (°C)')
            elif sensor == 'DO':
                ax1.set_ylabel('DO (mg/L)')
            elif sensor == 'turb':
                ax1.set_ylabel('Turbiditas (NTU)')
        else:
            for ax in [ax1, ax2]:
                ax.text(0.5, 0.5, 'Tidak ada data', ha='center', va='center', transform=ax.transAxes)
                ax.set_title(f'Sensor {sensor.upper()}', fontsize=14)

    for ax in axes.flatten():
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
        plt.setp(ax.get_xticklabels(), rotation=45, ha="right")

    plt.subplots_adjust(
        left=0.044,
        bottom=0.089,
        right=0.992,
        top=0.92,
        wspace=0.12,
        hspace=0.262
    )
    plt.show()

except Exception as e:
    print(f"Terjadi error saat memproses file: {e}")