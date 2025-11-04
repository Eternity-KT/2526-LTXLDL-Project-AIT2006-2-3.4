import pandas as pd
from datetime import datetime
from meteostat import Point, Daily
import openmeteo_requests
import requests_cache
from retry_requests import retry

# =============================================================================
# THIẾT LẬP THAM SỐ - TP. HỒ CHÍ MINH NĂM 2024
# =============================================================================
LATITUDE = 10.823      # Tọa độ TP. Hồ Chí Minh
LONGITUDE = 106.6296   # Tọa độ TP. Hồ Chí Minh
START_DATE = datetime(2024, 1, 1)
END_DATE = datetime(2024, 12, 31)

# =============================================================================
# 1. LẤY DỮ LIỆU THỜI TIẾT TỪ METEOSTAT
# =============================================================================
print("=" * 70)
print("Bắt đầu tải dữ liệu thời tiết từ Meteostat...")
print("=" * 70)

# Tạo điểm (Point) dựa trên tọa độ
location = Point(LATITUDE, LONGITUDE)

# Lấy dữ liệu hàng ngày (Daily)
data = Daily(location, START_DATE, END_DATE)
meteostat_data = data.fetch()

# Chọn các cột cần thiết
required_columns = ['tavg', 'prcp', 'wspd', 'wdir', 'pres']
weather_data = meteostat_data[required_columns]

# Đổi tên cột cho rõ ràng
weather_data = weather_data.rename(columns={
    'tavg': 'temperature_avg_C',
    'prcp': 'precipitation_mm',
    'wspd': 'wind_speed_kmh',
    'wdir': 'wind_direction_deg',
    'pres': 'pressure_hPa'
})

# Lưu dữ liệu thời tiết
meteostat_output = 'raw/meteostat_weather_data.csv'
weather_data.to_csv(meteostat_output)
print(f"✓ Đã lưu dữ liệu thời tiết tại: {meteostat_output}")
print(f"  Số dòng dữ liệu: {len(weather_data)}")
print("\nDữ liệu thời tiết (5 dòng đầu):")
print(weather_data.head())

# =============================================================================
# 2. LẤY DỮ LIỆU CHẤT LƯỢNG KHÔNG KHÍ TỪ OPEN-METEO
# =============================================================================
print("\n" + "=" * 70)
print("Bắt đầu tải dữ liệu chất lượng không khí từ Open-Meteo...")
print("=" * 70)

try:
    import requests
    import numpy as np
    
    # Thử nhiều URL khác nhau
    urls_to_try = [
        "https://air-quality.open-meteo.com/v1/air-quality",
        "http://air-quality.open-meteo.com/v1/air-quality",
        "https://api.open-meteo.com/v1/air-quality"
    ]
    
    params = {
        "latitude": LATITUDE,
        "longitude": LONGITUDE,
        "hourly": "pm10,pm2_5,uv_index,uv_index_clear_sky,carbon_monoxide,ozone,nitrogen_dioxide,sulphur_dioxide,dust",
        "start_date": START_DATE.strftime("%Y-%m-%d"),
        "end_date": END_DATE.strftime("%Y-%m-%d"),
        "timezone": "Asia/Bangkok"
    }

    print("Đang thử kết nối với Open-Meteo API...")
    data = None
    successful_url = None
    
    for url in urls_to_try:
        try:
            print(f"  Đang thử: {url}")
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()
            successful_url = url
            print(f"  ✓ Kết nối thành công!")
            break
        except Exception as url_error:
            print(f"  ✗ Thất bại: {type(url_error).__name__}")
            continue
    
    if data is None:
        raise Exception("Không thể kết nối với bất kỳ URL nào của Open-Meteo")
    
    print(f"✓ URL sử dụng: {successful_url}")
    print(f"✓ Tọa độ: {data['latitude']}°N {data['longitude']}°E")
    print(f"✓ Độ cao: {data['elevation']} m")
    print(f"✓ Múi giờ: {data['timezone']} ({data['timezone_abbreviation']})")
    
    # Xử lý dữ liệu hourly
    hourly = data['hourly']
    
    hourly_data = {
        "date": pd.to_datetime(hourly['time']),
        "pm10": hourly.get('pm10', [None] * len(hourly['time'])),
        "pm2_5": hourly.get('pm2_5', [None] * len(hourly['time'])),
        "uv_index": hourly.get('uv_index', [None] * len(hourly['time'])),
        "uv_index_clear_sky": hourly.get('uv_index_clear_sky', [None] * len(hourly['time'])),
        "carbon_monoxide": hourly.get('carbon_monoxide', [None] * len(hourly['time'])),
        "ozone": hourly.get('ozone', [None] * len(hourly['time'])),
        "nitrogen_dioxide": hourly.get('nitrogen_dioxide', [None] * len(hourly['time'])),
        "sulphur_dioxide": hourly.get('sulphur_dioxide', [None] * len(hourly['time'])),
        "dust": hourly.get('dust', [None] * len(hourly['time']))
    }
    
    # Tạo DataFrame
    air_quality_hourly = pd.DataFrame(data=hourly_data)
    
    print(f"\n📊 Thống kê dữ liệu hourly:")
    print(f"  - Tổng số dòng: {len(air_quality_hourly)}")
    print(f"  - PM10: {air_quality_hourly['pm10'].notna().sum()} giá trị")
    print(f"  - PM2.5: {air_quality_hourly['pm2_5'].notna().sum()} giá trị")
    print(f"  - UV Index: {air_quality_hourly['uv_index'].notna().sum()} giá trị")
    
    # Chuyển sang dữ liệu hàng ngày (lấy trung bình)
    air_quality_hourly['date_only'] = air_quality_hourly['date'].dt.date
    air_quality_daily = air_quality_hourly.groupby('date_only').agg({
        'pm10': 'mean',
        'pm2_5': 'mean',
        'uv_index': 'max',  # UV index lấy max trong ngày
        'uv_index_clear_sky': 'max',
        'carbon_monoxide': 'mean',
        'ozone': 'mean',
        'nitrogen_dioxide': 'mean',
        'sulphur_dioxide': 'mean',
        'dust': 'mean'
    })

    # Lưu dữ liệu chất lượng không khí (hourly)
    openmeteo_hourly_output = 'raw/openmeteo_air_quality_hourly.csv'
    air_quality_hourly.to_csv(openmeteo_hourly_output, index=False)
    print(f"✓ Đã lưu dữ liệu chất lượng không khí (hourly) tại: {openmeteo_hourly_output}")
    print(f"  Số dòng dữ liệu: {len(air_quality_hourly)}")

    # Lưu dữ liệu chất lượng không khí (daily)
    openmeteo_daily_output = 'raw/openmeteo_air_quality_daily.csv'
    air_quality_daily.to_csv(openmeteo_daily_output)
    print(f"✓ Đã lưu dữ liệu chất lượng không khí (daily) tại: {openmeteo_daily_output}")
    print(f"  Số dòng dữ liệu: {len(air_quality_daily)}")

    print("\nDữ liệu chất lượng không khí (5 dòng đầu - daily average):")
    print(air_quality_daily.head())

    # Biến để đánh dấu dữ liệu Open-Meteo có sẵn
    has_air_quality_data = True

except Exception as e:
    print(f"⚠ LỖI: Không thể tải dữ liệu từ Open-Meteo API")
    print(f"   Chi tiết lỗi: {type(e).__name__}: {str(e)}")
    print(f"   Vui lòng kiểm tra kết nối mạng hoặc thử lại sau.")
    print(f"   Chương trình sẽ tiếp tục với chỉ dữ liệu thời tiết từ Meteostat.")
    has_air_quality_data = False
    air_quality_daily = None

# =============================================================================
# 3. KẾT HỢP DỮ LIỆU
# =============================================================================
if has_air_quality_data:
    print("\n" + "=" * 70)
    print("Kết hợp dữ liệu thời tiết và chất lượng không khí...")
    print("=" * 70)

    # Chuẩn bị index cho merge
    weather_data_reset = weather_data.copy()
    weather_data_reset['date'] = weather_data_reset.index.date

    air_quality_daily_reset = air_quality_daily.copy()
    air_quality_daily_reset['date'] = air_quality_daily_reset.index

    # Merge dữ liệu
    combined_data = pd.merge(
        weather_data_reset, 
        air_quality_daily_reset, 
        on='date', 
        how='outer'
    )
    combined_data.set_index('date', inplace=True)

    # Lưu dữ liệu kết hợp
    combined_output = 'raw/combined_weather_airquality_data.csv'
    combined_data.to_csv(combined_output)
    print(f"✓ Đã lưu dữ liệu kết hợp tại: {combined_output}")
    print(f"  Số dòng dữ liệu: {len(combined_data)}")

    print("\nDữ liệu kết hợp (5 dòng đầu):")
    print(combined_data.head())

print("\n" + "=" * 70)
if has_air_quality_data:
    print("HOÀN TẤT! Tất cả dữ liệu đã được tải và lưu thành công.")
else:
    print("HOÀN TẤT! Dữ liệu thời tiết đã được tải thành công.")
    print("Lưu ý: Không tải được dữ liệu chất lượng không khí từ Open-Meteo.")
print("=" * 70)