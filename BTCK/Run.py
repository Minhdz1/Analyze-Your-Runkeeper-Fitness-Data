import pandas as pd
import numpy as np
import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

# 1. Data preprocessing
# Đọc dữ liệu từ file CSV
df = pd.read_csv('random_runkeeper_data_with_dates.csv')

# Chuyển đổi cột 'Date' thành kiểu dữ liệu datetime
df['Date'] = pd.to_datetime(df['Date'])

# Xử lý giá trị thiếu nếu có
df.fillna(df.mean(), inplace=True)

# Lưu kết quả sau khi tiền xử lý
df.to_csv('preprocessed_runkeeper_data.csv', index=False)
print("Đã tiền xử lý dữ liệu và lưu vào file CSV mới.")

# 2. Plot running data
plt.figure(figsize=(10, 5))
plt.scatter(df['Pace (min/km)'], df['Calories (kcal)'], color='blue')
plt.title('Tốc độ chạy vs Lượng calo tiêu thụ')
plt.xlabel('Tốc độ chạy (min/km)')
plt.ylabel('Lượng calo tiêu thụ (kcal)')
plt.grid(True)
plt.show()

plt.figure(figsize=(10, 5))
plt.scatter(df['Pace (min/km)'], df['Duration (min)'], color='green')
plt.title('Tốc độ chạy vs Thời gian chạy')
plt.xlabel('Tốc độ chạy (min/km)')
plt.ylabel('Thời gian chạy (min)')
plt.grid(True)
plt.show()

plt.figure(figsize=(10, 5))
plt.scatter(df['Calories (kcal)'], df['Duration (min)'], color='red')
plt.title('Lượng calo tiêu thụ vs Thời gian chạy')
plt.xlabel('Lượng calo tiêu thụ (kcal)')
plt.ylabel('Thời gian chạy (min)')
plt.grid(True)
plt.show()

# 3. Running statistics
average_pace = df['Pace (min/km)'].mean()
average_calories = df['Calories (kcal)'].mean()
average_duration = df['Duration (min)'].mean()
total_duration = df['Duration (min)'].sum()
num_runs = df.shape[0]

print("\n*** Thống kê Chạy Bộ ***")
print(f"Tốc độ chạy trung bình: {average_pace:.2f} min/km")
print(f"Lượng calo tiêu thụ trung bình: {average_calories:.2f} kcal")
print(f"Thời gian chạy trung bình: {average_duration:.2f} phút")
print(f"Tổng thời gian chạy: {total_duration:.2f} phút")
print(f"Số lần chạy: {num_runs}")

# Thời gian trung bình mỗi ngày chạy
daily_running_time = df.groupby(pd.to_datetime(df['Date']).dt.date)['Duration (min)'].sum()
average_daily_running_time = daily_running_time.mean()
print(f"Thời gian trung bình mỗi ngày chạy: {average_daily_running_time:.2f} phút")

# 4. Visualization with averages
fig, ax = plt.subplots(3, 1, figsize=(10, 15))

df.groupby(df['Date'].dt.date)['Pace (min/km)'].mean().plot(ax=ax[0], title='Tốc độ chạy trung bình mỗi ngày', color='blue')
ax[0].set_ylabel('Pace (min/km)')

df.groupby(df['Date'].dt.date)['Calories (kcal)'].mean().plot(ax=ax[1], title='Lượng calo tiêu thụ trung bình mỗi ngày', color='green')
ax[1].set_ylabel('Calories (kcal)')

df.groupby(df['Date'].dt.date)['Duration (min)'].mean().plot(ax=ax[2], title='Thời gian chạy trung bình mỗi ngày', color='red')
ax[2].set_ylabel('Duration (min)')

plt.tight_layout()
plt.show()

# 5. Did I reach my goals?
days_met_goal = daily_running_time[daily_running_time >= 30].count()
total_days = daily_running_time.count()

print(f"\nSố ngày đạt mục tiêu chạy 30 phút: {days_met_goal} / {total_days} ngày")

# 6. Am I progressing?
first_week = df[df['Date'] < '2024-01-08']
last_week = df[df['Date'] >= '2024-01-24']

average_pace_first_week = first_week['Pace (min/km)'].mean()
average_pace_last_week = last_week['Pace (min/km)'].mean()

print(f"\nTốc độ chạy trung bình tuần đầu tiên: {average_pace_first_week:.2f} min/km")
print(f"Tốc độ chạy trung bình tuần cuối cùng: {average_pace_last_week:.2f} min/km")

if average_pace_last_week < average_pace_first_week:
    print("Bạn đang tiến bộ!")
else:
    print("Bạn cần cải thiện thêm!")

# 7. Training intensity
intensity_levels = pd.cut(df['Pace (min/km)'], bins=[0, 5, 6, 10], labels=['High', 'Medium', 'Low'])
df['Intensity'] = intensity_levels

print("\nPhân bố cường độ tập luyện:")
print(df['Intensity'].value_counts())

# 8. Detailed summary report
summary_report = {
    'Tổng số lần chạy': num_runs,
    'Tổng thời gian chạy (phút)': total_duration,
    'Tốc độ chạy trung bình (min/km)': average_pace,
    'Lượng calo tiêu thụ trung bình (kcal)': average_calories,
    'Thời gian chạy trung bình (phút)': average_duration,
    'Số ngày đạt mục tiêu chạy 30 phút': f"{days_met_goal} / {total_days}",
    'Cường độ tập luyện': df['Intensity'].value_counts().to_dict()
}

print("\n*** Báo cáo chi tiết ***")
for key, value in summary_report.items():
    print(f"{key}: {value}")

# 9. Fun facts
longest_run = df['Duration (min)'].max()
most_calories_burned = df['Calories (kcal)'].max()
best_pace = df['Pace (min/km)'].min()

print("\n*** Fun Facts ***")
print(f"Chạy lâu nhất: {longest_run} phút")
print(f"Nhiều calo nhất tiêu thụ: {most_calories_burned} kcal")
print(f"Nhịp độ tốt nhất: {best_pace:.2f} min/km")

# Hiển thị fun facts bằng biểu đồ
fig, ax = plt.subplots(1, 3, figsize=(15, 5))

# Biểu đồ chạy lâu nhất
ax[0].bar(['Longest Run'], [longest_run], color='blue')
ax[0].set_title('Chạy lâu nhất')
ax[0].set_ylabel('Thời gian (phút)')

# Biểu đồ nhiều calo nhất tiêu thụ
ax[1].bar(['Most Calories Burned'], [most_calories_burned], color='green')
ax[1].set_title('Nhiều calo nhất tiêu thụ')
ax[1].set_ylabel('Lượng calo (kcal)')

# Biểu đồ nhịp độ tốt nhất
ax[2].bar(['Best Pace'], [best_pace], color='red')
ax[2].set_title('Nhịp độ tốt nhất')
ax[2].set_ylabel('Nhịp độ (min/km)')

plt.tight_layout()
plt.show()

# 10. Linear Regression to predict Calories burned
X = df[['Pace (min/km)', 'Duration (min)']]
y = df['Calories (kcal)']

# Chia dữ liệu thành tập huấn luyện và tập kiểm tra
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Huấn luyện mô hình hồi quy tuyến tính
model = LinearRegression()
model.fit(X_train, y_train)

# Dự đoán trên tập kiểm tra
y_pred = model.predict(X_test)

# Đánh giá mô hình
mse = mean_squared_error(y_test, y_pred)
print(f"Mean Squared Error: {mse:.2f}")

# Hiển thị kết quả
plt.figure(figsize=(10, 5))
plt.scatter(y_test, y_pred)
plt.plot([y.min(), y.max()], [y.min(), y.max()], 'k--', lw=2)
plt.title('Calories: True vs Predicted')
plt.xlabel('True Values (Calories)')
plt.ylabel('Predicted Values (Calories)')
plt.grid(True)
plt.show()

