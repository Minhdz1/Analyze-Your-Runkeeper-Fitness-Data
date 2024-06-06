import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from gtts import gTTS



# Đọc dữ liệu từ file CSV
df = pd.read_csv('runkeeper_data_30_days.csv')
# Khởi tạo môi trường âm thanh cho pygame

# Kiểm tra và xử lý các giá trị thiếu nếu có
if df.isnull().values.any():
    df = df.dropna()  # Loại bỏ các dòng chứa giá trị thiếu
df['Duration'] = pd.to_timedelta(df['Duration']).dt.total_seconds()

# Tính toán K-means clustering
X = df[['Duration', 'Distance (km)']].values
kmeans = KMeans(n_clusters=3, random_state=42)
df['Cluster'] = kmeans.fit_predict(X)

# Biểu đồ cho dữ liệu chạy bộ
plt.figure(figsize=(10, 6))
plt.bar(df['Date'], df['Distance (km)'], color='skyblue')
plt.title('Running Distance Over 30 Days')
plt.xlabel('Date')
plt.ylabel('Distance (km)')
plt.xticks(rotation=45)
plt.grid(axis='y')
plt.tight_layout()
plt.show(block=False)

# Running statistics
total_distance = df['Distance (km)'].sum()
total_duration = pd.to_timedelta(df['Duration']).sum()
average_pace = total_duration / total_distance

print("Total Distance:", total_distance, "km")
print("Total Duration:", total_duration)
print("Average Pace:", average_pace)

# Biểu đồ thể hiện khoảng cách chạy bộ cùng với giá trị trung bình
plt.figure(figsize=(10, 6))
plt.bar(df['Date'], df['Distance (km)'], color='skyblue', label='Distance (km)')
plt.axhline(y=total_distance/len(df), color='r', linestyle='--', label='Average Distance')
plt.title('Running Distance Over 30 Days with Average')
plt.xlabel('Date')
plt.ylabel('Distance (km)')
plt.xticks(rotation=45)
plt.legend()
plt.grid(axis='y')
plt.tight_layout()
plt.show(block=False)

# Đạt được mục tiêu chưa?
goal_distance = 150
total_distance = df['Distance (km)'].sum()
if total_distance >= goal_distance:
    print("Congratulations! You reached your goal of", goal_distance, "km.")
else:
    print("You didn't reach your goal of", goal_distance, "km. Keep going!")

# Tiến triển của bạn
df['Distance Growth'] = df['Distance (km)'].diff() / df['Distance (km)'].shift(1)
plt.figure(figsize=(10, 6))
plt.bar(df['Date'], df['Distance Growth'], color='lightgreen')
plt.title('Distance Growth Rate Over 30 Days')
plt.xlabel('Date')
plt.ylabel('Distance Growth Rate')
plt.xticks(rotation=45)
plt.grid(axis='y')
plt.tight_layout()
plt.show(block=False)

# Training intensity
average_heart_rate = df['Average Heart Rate (bpm)'].mean()
training_intensity = average_heart_rate / average_pace.total_seconds()

print("Average Heart Rate:", average_heart_rate, "bpm")
print("Training Intensity:", training_intensity)

# Báo cáo tổng quan chi tiết
summary_report = df.describe()
print(summary_report)

# Thông tin thú vị
fun_facts = {
    "Total Distance": total_distance,
    "Max Distance in a Day": df['Distance (km)'].max(),
    "Min Distance in a Day": df['Distance (km)'].min(),
    "Average Heart Rate": df['Average Heart Rate (bpm)'].mean(),
    "Max Steps in a Day": df['Steps'].max(),
    "Min Steps in a Day": df['Steps'].min()
}
print("\nFun Facts:")
for fact, value in fun_facts.items():
    print(f"{fact}: {value}")

# Biểu đồ thể hiện tốc độ trung bình qua các ngày
plt.figure(figsize=(10, 6))
plt.bar(df['Date'], df['Average Pace (min/km)'], color='lightcoral')
plt.title('Average Pace Over 30 Days')
plt.xlabel('Date')
plt.ylabel('Average Pace (min/km)')
plt.xticks(rotation=45)
plt.grid(axis='y')
plt.tight_layout()
plt.show(block=False)

# Biểu đồ thể hiện nhịp tim trung bình qua các ngày
plt.figure(figsize=(10, 6))
plt.bar(df['Date'], df['Average Heart Rate (bpm)'], color='lightblue')
plt.title('Average Heart Rate Over 30 Days')
plt.xlabel('Date')
plt.ylabel('Average Heart Rate (bpm)')
plt.xticks(rotation=45)
plt.grid(axis='y')
plt.tight_layout()
plt.show(block=False)

# Biểu đồ thể hiện số bước chân qua các ngày
plt.figure(figsize=(10, 6))
plt.bar(df['Date'], df['Steps'], color='orange')
plt.title('Steps Over 30 Days')
plt.xlabel('Date')
plt.ylabel('Steps')
plt.xticks(rotation=45)
plt.grid(axis='y')
plt.tight_layout()
plt.show()


