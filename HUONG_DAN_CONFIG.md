# Hướng dẫn sử dụng `config.py`

File `config.py` chứa tất cả biến cố định dùng chung cho cả nhóm (seed, đường dẫn dữ liệu, ngưỡng phân lớp, tên cột feature...). Mục tiêu: khi ghép notebook của 3 người lại, mọi thứ khớp nhau, không phải sửa tay.

**Quy tắc quan trọng nhất: không copy giá trị từ file này ra gõ tay ở notebook khác. Luôn import và gọi qua `config.<tên_biến>`.** Nếu sau này cần đổi 1 giá trị, chỉ sửa đúng 1 chỗ trong `config.py` rồi commit, không ai phải tự đi sửa notebook của mình.

## 1. Cách import vào Colab

Mở notebook trên Colab, chạy đoạn này ở ô đầu tiên trước khi làm gì khác:

```python
!git clone https://github.com/<ten-repo-cua-nhom>.git
import sys
sys.path.append("/content/<ten-repo-cua-nhom>")

import config
```

Nếu bạn mở notebook ngay trong thư mục gốc của repo (không cần clone lại), chỉ cần dòng cuối:

```python
import config
```

Nếu đã pull code mới nhưng Colab vẫn dùng bản `config.py` cũ (do đã import trước đó), chạy lại:

```python
import importlib
importlib.reload(config)
```

## 2. Đọc dữ liệu và chia train/val/test

Luôn dùng đường dẫn và tỉ lệ chia từ `config`, không tự gõ số:

```python
import pandas as pd
from sklearn.model_selection import train_test_split

df = pd.read_csv(config.RAW_DATA_PATH)

train_df, temp_df = train_test_split(
    df, test_size=config.TEST_SIZE + config.VAL_SIZE, random_state=config.RANDOM_SEED
)
val_df, test_df = train_test_split(
    temp_df, test_size=config.TEST_SIZE / (config.TEST_SIZE + config.VAL_SIZE), random_state=config.RANDOM_SEED
)
```

Vì `RANDOM_SEED` cố định, ai chạy đoạn này cũng ra đúng cùng 1 cách chia dữ liệu.

## 3. Ngưỡng phân lớp (`LOW_THRESHOLD`, `HIGH_THRESHOLD`)

Người phụ trách EDA tính 2 ngưỡng này **một lần duy nhất, chỉ trên `train_df`**, sau đó cập nhật trực tiếp vào `config.py` (thay `None` bằng số thực) và commit lên repo.

Các notebook khác **không tự tính lại** ngưỡng — chỉ gọi:

```python
low, high = config.get_thresholds()
```

Nếu `LOW_THRESHOLD`/`HIGH_THRESHOLD` chưa được điền, hàm này sẽ báo lỗi ngay — đây là tín hiệu để kiểm tra lại xem đã pull bản `config.py` mới nhất chưa.

## 4. Tên cột sau tiền xử lý

- `TARGET_COLUMN`: tên cột nhãn phân loại (`"demand_level"`), giá trị 0/1/2 tương ứng `DEMAND_LEVEL_LABELS`
- `CYCLICAL_FEATURES`, `ONE_HOT_FEATURES`, `BINARY_FEATURES`, `NUMERIC_FEATURES`: nhóm cột theo cách xử lý tương ứng
- `DROP_COLUMNS`: các cột cần loại bỏ trước khi đưa vào mô hình
- `FEATURE_COLUMNS`: danh sách cột cuối cùng dùng làm input cho mô hình

**Lưu ý:** `FEATURE_COLUMNS` hiện chưa gồm các cột one-hot (`season_*`, `weathersit_*`) vì tên cột này phụ thuộc cách `pd.get_dummies` đặt tên. Người phụ trách tiền xử lý cần bổ sung thủ công các tên cột này vào `FEATURE_COLUMNS` trong `config.py` sau khi encode xong, rồi commit lại.

## 5. Xuất dữ liệu đã xử lý cho người tiếp theo dùng

Sau khi tiền xử lý xong, xuất ra đúng đường dẫn trong config, không đặt tên file khác:

```python
train_df.to_csv(config.PROCESSED_TRAIN_PATH, index=False)
val_df.to_csv(config.PROCESSED_VAL_PATH, index=False)
test_df.to_csv(config.PROCESSED_TEST_PATH, index=False)
```

Người làm phần mô hình chỉ cần đọc thẳng các file này, không cần chạy lại pipeline tiền xử lý:

```python
train_df = pd.read_csv(config.PROCESSED_TRAIN_PATH)
X_train = train_df[config.FEATURE_COLUMNS]
y_train = train_df[config.TARGET_COLUMN]
```

## 6. Quy ước đặt tên biến trong notebook

Đây là các tên biến dùng chung khi viết code (không nằm trong `config.py` vì đây là tên biến Python, không phải giá trị dữ liệu) — cả nhóm cần dùng đúng các tên này để khi ghép notebook không phải đổi tên lại:

| Biến | Ý nghĩa | Được tạo ở bước |
|---|---|---|
| `df` | DataFrame gốc, đọc thẳng từ `config.RAW_DATA_PATH`, chưa xử lý | EDA |
| `train_df`, `val_df`, `test_df` | 3 tập sau khi `train_test_split`, chưa tiền xử lý | EDA / đầu Preprocessing |
| `train_processed`, `val_processed`, `test_processed` | 3 tập sau khi tiền xử lý xong (đã có `FEATURE_COLUMNS` và `TARGET_COLUMN`) | Preprocessing |
| `X_train`, `X_val`, `X_test` | Ma trận feature, luôn lấy từ `train_processed[config.FEATURE_COLUMNS]` (tương tự cho val/test) | Modeling |
| `y_train`, `y_val`, `y_test` | Cột nhãn, luôn lấy từ `train_processed[config.TARGET_COLUMN]` (tương tự cho val/test) | Modeling |
| `model` | Mô hình đang huấn luyện trong ô hiện tại (nếu so sánh nhiều mô hình, đặt tên cụ thể: `model_logreg`, `model_rf`, `model_xgb`) | Modeling |
| `y_pred` | Kết quả dự đoán của `model` trên `X_test` (hoặc `y_pred_val` nếu dự đoán trên tập val) | Modeling |

**Quy tắc chung:**
- Không viết tắt khác đi (VD không dùng `df_train`, `Xtr`, `traindf`) — chỉ dùng đúng tên trong bảng trên
- Biến trung gian riêng của từng người (không bàn giao cho phần khác) thì đặt tên tự do, không cần theo bảng này
- Nếu cần thêm biến dùng chung mới không có trong bảng, thêm vào bảng này và báo nhóm trước khi dùng trong phần bàn giao

## 7. Khi nào cần sửa `config.py`

| Tình huống | Việc cần làm |
|---|---|
| Vừa tính xong ngưỡng phân lớp | Điền `LOW_THRESHOLD`, `HIGH_THRESHOLD`, commit ngay |
| Vừa one-hot encode xong | Thêm tên cột mới vào `FEATURE_COLUMNS`, commit |
| Muốn đổi tỉ lệ train/val/test | Sửa `TEST_SIZE`/`VAL_SIZE` trong config, báo cả nhóm chạy lại từ đầu |
| Muốn thử `RANDOM_SEED` khác | Bàn thống nhất cả nhóm trước, vì đổi seed sẽ làm toàn bộ train/val/test split thay đổi |

**Nguyên tắc chung:** ai sửa `config.py` xong đều commit và báo trong nhóm ngay, vì mọi notebook khác đều phụ thuộc vào file này để cho ra kết quả nhất quán.
