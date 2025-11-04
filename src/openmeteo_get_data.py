import pandas as pd
import numpy as np

print("=" * 70)
print("CHUYỂN ĐỔI DỮ LIỆU CHẤT LƯỢNG KHÔNG KHÍ: HOURLY → DAILY")
print("=" * 70)

# =============================================================================
# 1. ĐỌC DỮ LIỆU HOURLY
# =============================================================================
print("\n📂 Đọc dữ liệu hourly từ file...")
input_file = 'raw/open-meteo-hourly-AQ.csv'

# Đọc file, bỏ qua 2 dòng header đầu tiên (metadata)
df_hourly = pd.read_csv(input_file, skiprows=2)

print(f"✓ Đã đọc {len(df_hourly)} dòng dữ liệu hourly")
print(f"✓ Các cột: {list(df_hourly.columns)}")

# =============================================================================
# 2. TIỀN XỬ LÝ DỮ LIỆU
# =============================================================================
print("\n🔧 Tiền xử lý dữ liệu...")

# Chuyển đổi cột time sang datetime
df_hourly['time'] = pd.to_datetime(df_hourly['time'])

# Tạo cột date (chỉ lấy ngày, bỏ giờ)
df_hourly['date'] = df_hourly['time'].dt.date

print(f"✓ Khoảng thời gian: {df_hourly['date'].min()} đến {df_hourly['date'].max()}")

# Lấy danh sách các cột chỉ số (bỏ cột time và date)
indicator_columns = [col for col in df_hourly.columns if col not in ['time', 'date']]
print(f"✓ Số chỉ số: {len(indicator_columns)}")
print(f"  Các chỉ số: {indicator_columns}")

# =============================================================================
# 3. CHUYỂN ĐỔI SANG DỮ LIỆU DAILY
# =============================================================================
print("\n📊 Chuyển đổi sang dữ liệu theo ngày...")

# Định nghĩa cách tính toán cho từng loại chỉ số
# - PM10, PM2.5, CO, CO2, Ozone: lấy TRUNG BÌNH (mean)
# - UV Index: lấy GIÁ TRỊ LỚN NHẤT (max) trong ngày

aggregation_dict = {}
for col in indicator_columns:
    # Nếu là UV index thì lấy max, còn lại lấy mean
    if 'uv_index' in col.lower() or 'uv index' in col.lower():
        aggregation_dict[col] = 'max'
    else:
        aggregation_dict[col] = 'mean'

# Thực hiện group by date và aggregate
df_daily = df_hourly.groupby('date').agg(aggregation_dict).reset_index()

# Làm tròn tất cả các cột số đến 2 chữ số thập phân
for col in indicator_columns:
    df_daily[col] = df_daily[col].round(2)

# Đổi tên cột date thành time để nhất quán
df_daily.rename(columns={'date': 'time'}, inplace=True)

print(f"✓ Đã tạo {len(df_daily)} dòng dữ liệu daily")
print(f"✓ Đã làm tròn tất cả giá trị đến 2 chữ số thập phân")

# =============================================================================
# 4. HIỂN THỊ THỐNG KÊ
# =============================================================================
print("\n📈 Thống kê dữ liệu daily:")
for col in indicator_columns:
    valid_count = df_daily[col].notna().sum()
    if valid_count > 0:
        mean_val = df_daily[col].mean()
        min_val = df_daily[col].min()
        max_val = df_daily[col].max()
        print(f"  • {col}:")
        print(f"      Số ngày có dữ liệu: {valid_count}/{len(df_daily)}")
        print(f"      Trung bình: {mean_val:.2f}, Min: {min_val:.2f}, Max: {max_val:.2f}")
    else:
        print(f"  • {col}: Không có dữ liệu")

# =============================================================================
# 5. LƯU DỮ LIỆU DAILY
# =============================================================================
print("\n💾 Lưu dữ liệu daily...")
output_file = 'raw/open-meteo-daily-AQ.csv'

# Lưu file với giá trị NaN được hiển thị rõ ràng
df_daily.to_csv(output_file, index=False, na_rep='NaN')

print(f"✓ Đã lưu dữ liệu tại: {output_file}")
print(f"✓ Các ô thiếu giá trị đã được điền 'NaN'")

# =============================================================================
# 6. HIỂN THỊ MẪU DỮ LIỆU
# =============================================================================
print("\n📋 Dữ liệu daily (10 dòng đầu tiên):")
print(df_daily.head(10).to_string())

print("\n" + "=" * 70)
print("✅ HOÀN TẤT! Dữ liệu đã được chuyển đổi thành công.")
print("=" * 70)
print(f"\n📁 File đầu vào:  {input_file}")
print(f"📁 File đầu ra:   {output_file}")
print(f"📊 Số ngày:       {len(df_daily)} ngày")
print(f"📊 Số chỉ số:     {len(indicator_columns)} chỉ số")
