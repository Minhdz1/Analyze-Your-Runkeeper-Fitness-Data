import csv
from datetime import datetime, timedelta
import random


# Hàm tạo dữ liệu mẫu cho mỗi ngày
def generate_activity_data(start_date, num_days):
    activities = ["Running", "Cycling", "Walking"]
    data = [["Date", "Time", "Activity", "Distance (km)", "Duration", "Average Pace (min/km)", "Calories Burned",
             "Average Heart Rate (bpm)", "Steps"]]

    for i in range(num_days):
        date = start_date + timedelta(days=i)
        time = datetime.strptime("06:30:00", "%H:%M:%S") + timedelta(minutes=random.randint(0, 60))
        activity = random.choice(activities)

        if activity == "Running":
            distance = round(random.uniform(3, 10), 2)
            pace = round(random.uniform(4.5, 6.5), 2)
            duration = round(distance * pace, 2)
            calories = round(distance * 60, 2)
            heart_rate = random.randint(140, 160)
            steps = round(distance * 1200)

        elif activity == "Cycling":
            distance = round(random.uniform(10, 40), 2)
            pace = round(random.uniform(2.5, 4.5), 2)
            duration = round(distance * pace, 2)
            calories = round(distance * 25, 2)
            heart_rate = random.randint(130, 150)
            steps = 0

        else:  # Walking
            distance = round(random.uniform(2, 5), 2)
            pace = round(random.uniform(8.5, 10.5), 2)
            duration = round(distance * pace, 2)
            calories = round(distance * 40, 2)
            heart_rate = random.randint(100, 120)
            steps = round(distance * 1400)

        data.append([
            date.strftime("%Y-%m-%d"),
            time.strftime("%H:%M:%S"),
            activity,
            distance,
            f"{int(duration // 60):02d}:{int(duration % 60):02d}:00",
            f"{int(pace)}:{int((pace * 60) % 60):02d}",
            calories,
            heart_rate,
            steps
        ])

    return data


# Tạo dữ liệu mẫu từ ngày 1 đến ngày 30
start_date = datetime.strptime("2024-06-01", "%Y-%m-%d")
num_days = 30
data = generate_activity_data(start_date, num_days)

# Tạo file CSV
with open('runkeeper_data_30_days.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(data)

print("File CSV đã được tạo thành công.")
