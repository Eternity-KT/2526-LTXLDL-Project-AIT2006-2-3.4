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
│   ├── clustering_summary.csv       # Kết quả phân cụm K-Means
│   ├── pm25_forecasting_results.csv # Kết quả dự báo PM2.5
│   ├── report-AIT2006-2-3.4-final.tex  # Báo cáo kỹ thuật LaTeX
│   └── report-AIT2006-2-3.4-final.pdf  # Báo cáo kỹ thuật PDF (29 trang)
│
├── figures/                          # Hình ảnh / Figures (15 files)
│   ├── 01_time_series.pdf           # Meteogram tổng hợp
│   ├── 02_uv_index.pdf              # UV Index theo thời gian
│   ├── 03_Pm25_distribution.pdf     # Phân bố PM2.5
│   ├── 04_monthly_boxplot.pdf       # Boxplot PM2.5 theo tháng
│   ├── 05_correlation_matrix.pdf    # Ma trận tương quan
│   ├── 06_wind_pm25_scatter.pdf     # Gió vs PM2.5
│   ├── 7_temp_ozone_scatter.pdf     # Nhiệt độ vs Ozone
│   ├── 8_pm25_vs_pm10_timeseries.pdf # So sánh PM2.5 và PM10
│   ├── 09_aqi_category_stacked_bar.pdf # Phân loại AQI theo tháng
│   ├── 10_kmeans_pca_scatter_yellow_rain.pdf    # PCA scatter clustering
│   ├── 11_kmeans_calendar_heatmap_yellow.pdf # Calendar heatmap clustering
│   ├── 12_feature_importance.pdf    # Feature importance dự báo
│   ├── 13_pm25_predictions.pdf      # Kết quả dự báo PM2.5
│   ├── 14_timeseries_pm25.pdf       # Time series PM2.5
│   └── 15_case_study_rank2_*.pdf    # Case study anomaly detection
│
└── src/                              # Mã nguồn / Source code
    ├── 00_convert_aq_hourly_to_daily.py # Chuyển đổi AQ hourly sang daily
    ├── 01_weather_data_cleaning.ipynb
    ├── 02_airquality_data_cleaning.ipynb
    ├── 03_merge_and_sync.ipynb
    ├── 04_statistics_and_aggregation.ipynb
    ├── 05_visualization.ipynb
    ├── 06_pm25_forecasting.ipynb    # 🎯 BONUS: Dự báo PM2.5
    ├── 07_advanced_analysis.ipynb   # 🎯 BONUS: Anomaly detection
    ├── 08_kmeans_clustering.ipynb   # 🎯 BONUS: K-Means clustering
    └── get_weather_data_meteostat.py
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
- Output: `final_combined_data.csv` (366 ngày)

### 4️⃣ **Statistics and Aggregation** (`04_statistics_and_aggregation.ipynb`)
- Tính toán thống kê mô tả (mean, median, std, percentiles)
- Tổng hợp theo ngày/tuần/tháng
- Tính normalized index và AQI
- Output: `statistics_summary.csv`, các file aggregation

### 5️⃣ **Visualization** (`05_visualization.ipynb`)
- Tạo các biểu đồ phân tích xu hướng và mối quan hệ
- Meteogram, scatter plots, correlation matrix, AQI categories
- Output: 9 PDF files trong `figures/`

### 6️⃣ **PM2.5 Forecasting** (`06_pm25_forecasting.ipynb`) 🎯 **BONUS**
- Dự báo PM2.5 cho **ngày tiếp theo** bằng Linear Regression
- Feature engineering: lag features, rolling averages, weather, temporal
- Metrics: MAE, MAPE, RMSE, R²
- Output: `pm25_forecasting_results.csv`, 3 visualization PDFs

### 7️⃣ **Advanced Analysis** (`07_advanced_analysis.ipynb`) 🎯 **BONUS**
- Phát hiện anomalies bằng Isolation Forest
- Case study analysis cho các ngày ô nhiễm cao
- Output: 2 case study PDFs

### 8️⃣ **K-Means Clustering** (`08_kmeans_clustering.ipynb`) 🎯 **BONUS**
- Phân cụm điều kiện môi trường (4 clusters)
- PCA visualization và calendar heatmap
- Output: `clustering_summary.csv`, 2 visualization PDFs

---

## 🎯 Tính năng Bonus / Bonus Features

### 1. **Dự báo PM2.5 ngày tiếp theo / Next-Day PM2.5 Forecasting**

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

### 2. **Phân cụm K-Means / K-Means Clustering**

**Algorithm:** K-Means với K=4 clusters  
**Features:** Nhiệt độ, lượng mưa, tốc độ gió, UV Index, PM2.5, O₃  
**Clusters:**
- Mưa (59 ngày, 16.7%)
- Mưa - Bụi cao (94 ngày, 26.6%)
- Nóng - Sạch (119 ngày, 33.6%)
- Trung tính/Giao mùa (82 ngày, 23.2%)

### 3. **Phát hiện bất thường / Anomaly Detection**

**Algorithm:** Isolation Forest  
**Output:** Case studies cho ngày ô nhiễm cao nhất và top anomalies

---

## 🛠️ Dependencies

```txt
pandas
numpy
matplotlib
seaborn
scikit-learn
meteostat
```

Install: `pip install -r requirements.txt`

---

## 📊 Kết quả / Results

- **Data Coverage:** 366 ngày (2024-01-01 đến 2024-12-31)
- **Training Samples:** ~280 ngày
- **Testing Samples:** ~70 ngày
- **Forecast Target:** PM2.5 ngày tiếp theo
- **Visualizations:** 15 PDF files trong `figures/`
- **Technical Report:** 29 trang với tất cả phân tích và hình ảnh
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
- Năm 2024: Năm nhuận (366 ngày)
- Báo cáo kỹ thuật: 29 trang PDF với 16 hình ảnh minh họa
