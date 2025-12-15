# 2526-LTXLDL-Project-AIT2006-2-3.4
# Weather and Air Quality Data Processing Project

## 📋 Mô tả dự án / Project Description

Dự án xử lý và phân tích dữ liệu thời tiết và chất lượng không khí cho khu vực Hồ Chí Minh (10.823°N, 106.6296°E) trong năm 2024. Bao gồm làm sạch dữ liệu, tổng hợp thống kê, và dự báo PM2.5 cho ngày tiếp theo.

This project processes and analyzes weather and air quality data for Ho Chi Minh City (10.823°N, 106.6296°E) throughout 2024, including data cleaning, statistical aggregation, and next-day PM2.5 forecasting.

---

## 📁 Cấu trúc thư mục / Directory Structure

```
├── raw/                              # Dữ liệu gốc / Raw data
│   ├── meteostat_weather_data.csv   # Dữ liệu thời tiết từ Meteostat
│   └── open-meteo-hourly-AQ.csv     # Dữ liệu chất lượng không khí theo giờ
│
├── processed/                        # Dữ liệu đã xử lý / Processed data
│   ├── weather_cleaned.csv          # Dữ liệu thời tiết đã làm sạch
│   ├── airquality_cleaned.csv       # Dữ liệu chất lượng không khí đã làm sạch
│   ├── open-meteo-daily-AQ.csv      # Dữ liệu chất lượng không khí theo ngày
│   ├── final_combined_data.csv      # Dữ liệu kết hợp cuối cùng
│   ├── daily_weather_aqi_*.csv      # Tổng hợp theo ngày
│   ├── weekly_weather_aqi_*.csv     # Tổng hợp theo tuần
│   └── monthly_weather_aqi_*.csv    # Tổng hợp theo tháng
│
├── reports/                          # Báo cáo / Reports
│   ├── qa_weather_summary.csv       # Tóm tắt QA dữ liệu thời tiết
│   ├── qa_airquality_summary.csv    # Tóm tắt QA dữ liệu chất lượng không khí
│   ├── merge_summary.csv            # Tóm tắt quá trình merge
│   ├── statistics_summary.csv       # Thống kê mô tả
│   ├── statistics_metadata.csv      # Metadata thống kê
│   └── pm25_forecasting_results.csv # Kết quả dự báo PM2.5
│
├── figures/                          # Hình ảnh / Figures
│   ├── 05_timeseries_pm25.pdf       # Biểu đồ chuỗi thời gian PM2.5
│   ├── 05_pm25_predictions.pdf      # Biểu đồ dự báo PM2.5
│   └── 05_feature_importance.pdf    # Biểu đồ độ quan trọng của features
│
└── src/                              # Mã nguồn / Source code
    ├── 01_weather_data_cleaning.ipynb
    ├── 02_airquality_data_cleaning.ipynb
    ├── 03_merge_and_sync.ipynb
    ├── 04_statistics_and_aggregation.ipynb
    ├── 05_pm25_forecasting.ipynb    # 🎯 BONUS: Dự báo PM2.5
    ├── get_weather_data_meteostat.py
    ├── convert_aq_hourly_to_daily.py
    └── visualization.ipynb
```

---

## 🔄 Quy trình phân tích / Analysis Workflow

### 1️⃣ **Weather Data Cleaning** (`01_weather_data_cleaning.ipynb`)
- Làm sạch dữ liệu thời tiết từ Meteostat
- Xử lý giá trị thiếu và outliers
- Output: `weather_cleaned.csv`

### 2️⃣ **Air Quality Data Cleaning** (`02_airquality_data_cleaning.ipynb`)
- Chuyển đổi dữ liệu AQ từ hourly sang daily
- Làm sạch và chuẩn hóa dữ liệu
- Output: `airquality_cleaned.csv`, `open-meteo-daily-AQ.csv`

### 3️⃣ **Merge and Synchronization** (`03_merge_and_sync.ipynb`)
- Kết hợp dữ liệu thời tiết và chất lượng không khí
- Đồng bộ hóa timestamps
- Output: `final_combined_data.csv` (368 ngày)

### 4️⃣ **Statistics and Aggregation** (`04_statistics_and_aggregation.ipynb`)
- Tính toán thống kê mô tả (mean, median, std, percentiles)
- Tổng hợp theo ngày/tuần/tháng
- Tính normalized index và AQI
- Output: `statistics_summary.csv`, các file aggregation

### 5️⃣ **PM2.5 Forecasting** (`05_pm25_forecasting.ipynb`) 🎯 **BONUS**
- Dự báo PM2.5 cho **ngày tiếp theo** bằng Linear Regression
- Feature engineering: lag features, rolling averages, weather, temporal
- Metrics: MAE, MAPE, RMSE, R²
- Output: `pm25_forecasting_results.csv`, visualization PDFs

---

## 🎯 Tính năng Bonus / Bonus Features

### **Dự báo PM2.5 ngày tiếp theo / Next-Day PM2.5 Forecasting**

**Model:** Linear Regression  
**Features (15):**
- Lag features: PM2.5 của 1, 2, 3 ngày trước
- Rolling averages: trung bình 3 ngày, 7 ngày
- Weather: nhiệt độ, mưa, gió, áp suất (hôm nay)
- Air quality: PM10, O₃, CO (hôm nay)
- Temporal: ngày trong tuần, ngày trong tháng, tháng (của ngày dự báo)

**Performance Metrics:**
- MAE (Mean Absolute Error): μg/m³
- MAPE (Mean Absolute Percentage Error): %
- RMSE (Root Mean Squared Error): μg/m³
- R² Score: 0-1

**Data Split:** 80% training / 20% testing (chronological split)

---

## 🛠️ Dependencies

```txt
pandas
numpy
matplotlib
seaborn
scikit-learn
```

Install: `pip install -r requirements.txt`

---

## 📊 Kết quả / Results

- **Data Coverage:** 368 ngày (2024-01-01 đến 2024-12-31)
- **Training Samples:** ~290 ngày
- **Testing Samples:** ~71 ngày
- **Forecast Target:** PM2.5 ngày tiếp theo
- **All visualizations:** PDF format trong `figures/`
- **All reports:** CSV format trong `reports/`

---

## 👥 Thông tin / Information

**Course:** AIT2006 - Data Processing  
**Project ID:** 2526-LTXLDL-PROJECT-AIT2006-2-3.4  
**Year:** 2024-2025

---

## 📝 Ghi chú / Notes

- Dữ liệu thời tiết: Meteostat API
- Dữ liệu chất lượng không khí: Open-Meteo API
- Tọa độ: 10.823°N, 106.6296°E (Hồ Chí Minh)
- Timezone: UTC+7
- Branch cho bonus: `feature/forecasting-bonus`
