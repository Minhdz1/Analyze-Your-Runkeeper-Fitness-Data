import pandas as pd
import numpy as np

# Tạo dữ liệu ngẫu nhiên
num_records = 100

data = {
    'Pace (min/km)': np.random.uniform(4.0, 7.0, num_records),
    'Calories (kcal)': np.random.randint(200, 500, num_records),
    'Duration (min)': np.random.randint(20, 60, num_records),
    'Date': np.random.choice(pd.date_range('2024-01-01', '2024-01-31'), size=num_records)
}

df = pd.DataFrame(data)
df.to_csv('random_runkeeper_data_with_dates.csv', index=False)
print("Đã tạo file CSV với dữ liệu ngẫu nhiên.")
