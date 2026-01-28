# Mosaic 練習專案（2024/01/06）

使用 **OpenCV**、**PIL** 與 **scipy** 實作多種影像處理練習，包含：
- **Hw2**：圖片切割與隨機空格
- **Hw3**：Photomosaic（利用顏色相近度與 K-D Tree 拼貼）
- **Hw4**：邊緣偵測（Canny Edge Detection）
- **mosaic-master**：完整的 Photomosaic 實作（使用小圖片資料集拼成大圖）

---

## 📁 專案結構

```
mosaic_opencv/
├── assets/                    # 輸入圖片（如 hw2_pic1.jpg, cats_pic.png）
├── results/                   # 輸出結果
├── mosaic-master/
│   └── mosaic-master/
│       ├── main.py            # Photomosaic 主程式
│       ├── dataset/           # 小圖片資料集（347 張 Pokemon 圖片）
│       ├── input.jpg          # 輸入圖片
│       └── output.jpg         # 輸出結果
├── hw2.ipynb                  # 作業 2：圖片切割與隨機空格
├── hw3.ipynb                  # 作業 3：Photomosaic（顏色相近）
├── hw4.ipynb                  # 作業 4：邊緣偵測
├── montage.ipynb              # Montage 函式實作
├── test1.ipynb                # OpenCV 測試
└── Hw總表.txt                 # 作業總覽
```

---

## 🎯 功能說明

### 1. **Photomosaic（馬賽克拼貼）**
將一張大圖分割成許多小方塊，每個方塊用資料集中**顏色最接近**的小圖片替換，形成由多張小圖組成的大圖效果。

#### 實作檔案
- `mosaic-master/mosaic-master/main.py`
- `montage.ipynb`（使用 PIL 與 K-D Tree）
- `hw3.ipynb`（整合切割與 montage）

#### 原理
1. 讀取輸入圖片（如 `input.jpg`）並取得尺寸
2. 載入資料集中所有小圖片（`dataset/` 資料夾）
3. 調整所有小圖為固定大小（預設 20×20 或 10×10）
4. 計算每張小圖的**平均顏色**（RGB）
5. 將輸入圖片分割成多個方塊
6. 對每個方塊：
   - 計算方塊的平均顏色
   - 使用 **歐幾里得距離（Euclidean Distance）** 或 **K-D Tree** 找出資料集中最接近的小圖
   - 用該小圖替換方塊
7. 輸出結果圖片

#### 使用範例
```python
# 使用 main.py（需先準備 input.jpg 與 dataset/ 資料夾）
python mosaic-master/mosaic-master/main.py

# 使用 montage 函式（在 Jupyter Notebook 中）
montage("assets/hw2_pic1.jpg", "mosaic-master/mosaic-master/dataset/*", "output.jpg", (10, 10))
```

#### 參數調整
- **`piece_size`**（在 `main.py` 第 8 行）：方塊大小（數值越小，輸出越細緻但計算量越大）
- **`tile_size`**（在 `montage.ipynb`）：拼貼方塊尺寸 `(width, height)`

#### 資料集說明
- 使用 [Kaggle Pokemon 資料集](https://www.kaggle.com/datasets/sachsene/pokemons)（經過修改）
- 共 347 張圖片（`.jpg`、`.png`、`.jpeg`）
- 部分圖片需注意 **Image Mode**（RGB、RGBA、P），程式已處理透明度警告

---

### 2. **Hw2：圖片切割與隨機空格**
將圖片切成指定格子數，並隨機移除一些方塊（留白）。

#### 實作檔案
- `hw2.ipynb`

#### 功能
1. **`slice_matrix(shape, threshold)`**：產生隨機 0/1 矩陣（1 代表保留方塊）
2. **`revised_slice_matrix(shape, threshold)`**：避免整行或整列全為空白
3. **`crop_img(original_img_path, result_img_path)`**：根據矩陣切割圖片並留白

#### 使用範例
```python
# 設定切割數量
height_block_count = 10
width_block_count = 15

# 產生隨機切割矩陣（避免整行空白）
s_matrix = revised_slice_matrix((height_block_count, width_block_count))

# 執行切割
crop_img('assets/hw2_pic1.jpg', 'results/hw2_output.jpg')
```

---

### 3. **Hw3：Montage-1（顏色相近拼貼）**
結合 Hw2 的切割與 Photomosaic，並使用 **K-D Tree** 加速顏色匹配。

#### 實作檔案
- `hw3.ipynb`

#### 流程
1. 先對輸入圖片執行 `montage()` 生成拼貼圖
2. 再使用 `crop_img()` 隨機移除部分方塊
3. 輸出結果到 `results/hw3_output_revised.jpg`

#### 使用範例
```python
montage('assets/hw2_pic1.jpg', "mosaic-master/mosaic-master/dataset/*", "results/hw3_mont2_output.jpg", (10, 10))    
crop_img('results/hw3_mont2_output.jpg', 'results/hw3_output_revised.jpg')
```

---

### 4. **Hw4：邊緣偵測（Canny Edge Detection）**
使用 **Canny 邊緣偵測** 找出圖片中的邊緣輪廓。

#### 實作檔案
- `hw4.ipynb`

#### 功能
1. 將圖片轉為灰階
2. 使用高斯模糊（Gaussian Blur）去噪
3. 使用 Canny 演算法偵測邊緣

#### 使用範例
```python
import cv2

def edge_detection(Main_img, result_path):
    gray = cv2.cvtColor(Main_img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    result = cv2.Canny(blurred, 30, 150)
    
    cv2.imshow('Input', Main_img)
    cv2.imshow('Result', result)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

Mainimg = cv2.imread('assets/hw2_pic1.jpg', -1)
edge_detection(Mainimg, 'results/hw4_output.jpg')
```

---

## 🔧 環境需求

### Python 套件
```bash
pip install opencv-python numpy pillow scipy
```

### 套件版本參考
- `opencv-python`（cv2）
- `numpy`
- `pillow`（PIL）
- `scipy`（spatial.KDTree）

---

## 🚀 快速開始

### 1. 準備資料
```bash
# 確保以下資料存在
mosaic-master/mosaic-master/dataset/    # 小圖片資料集（至少數十張）
assets/hw2_pic1.jpg                     # 輸入圖片
```

### 2. 執行 Photomosaic
```bash
cd mosaic-master/mosaic-master
# 確保有 input.jpg
python main.py
# 輸出：output.jpg
```

### 3. 執行作業 Notebook
```bash
jupyter notebook
# 開啟 hw2.ipynb / hw3.ipynb / hw4.ipynb
```

---

## 📊 輸出結果示意

### Photomosaic 效果
| 輸入圖片 | 輸出拼貼圖 |
|---------|-----------|
| `input.jpg` | `output.jpg` |
| ![](mosaic-master/mosaic-master/input.jpg) | ![](mosaic-master/mosaic-master/output.jpg) |

### Hw2 切割效果
| 原圖 | 隨機空格切割 |
|------|-------------|
| `hw2_pic1.jpg` | `hw2_output.jpg` |

### Hw3 拼貼+切割
| 原圖 | 拼貼後切割 |
|------|-----------|
| `hw2_pic1.jpg` | `hw3_output_revised.jpg` |

### Hw4 邊緣偵測
| 原圖 | 邊緣圖 |
|------|--------|
| `hw2_pic1.jpg` | `hw4_output.jpg` |

---

## 🧠 演算法說明

### 1. 顏色匹配（Euclidean Distance）
```python
# 計算顏色差異
euclid_dist = np.linalg.norm(piece_color - avg_color, axis=1)
index = np.argmin(euclid_dist)  # 找最小距離
```

### 2. K-D Tree 加速搜尋（hw3）
```python
from scipy import spatial

# 建立 K-D Tree（資料集顏色）
tree = spatial.KDTree(colors)

# 快速查詢最接近的顏色
closest_tiles = np.zeros((height, width), dtype=np.uint32)
for i in range(height):
    for j in range(width):
        closest = tree.query(resized_photo.getpixel((j, i)))
        closest_tiles[i, j] = closest[1]
```

---

## ⚠️ 注意事項

1. **圖片模式問題**：部分 PNG 圖片為 **Palette Mode（P）**，需轉為 RGB：
   ```python
   tile = Image.open(path)
   if tile.mode != 'RGB':
       tile = tile.convert('RGB')
   ```

2. **資料集品質**：小圖片顏色多樣性越高，拼貼效果越好

3. **計算時間**：`piece_size` 越小（如 5×5），計算量越大，建議從 20×20 開始測試

4. **圖片尺寸**：輸入圖片應能整除 `piece_size`，否則會裁切邊緣

---

## 📝 作業總覽（Hw總表.txt）

```
Hw1 - Jupyter install, conda, network
Hw2 - 切成給定格子，隨機取去一些空格
Hw3 - Montage-1（利用 tile 的顏色相近，採 K-D tree 來作鑲切）
Hw4 - Montage-2（觀察主圖的邊緣，用邊緣相近）
```

---

## 🔗 參考資源

- [Snivy Pokemon 4K Wallpaper](https://wall.alphacoders.com/tag/4k-snivy-%28pokemon%29-wallpapers?lang=Dutch)（範例輸入圖片）
- [Kaggle Pokemon Dataset](https://www.kaggle.com/datasets/sachsene/pokemons)（資料集來源）
- OpenCV Canny Edge Detection：[官方文件](https://docs.opencv.org/4.x/da/d22/tutorial_py_canny.html)

---

## 📜 授權（License）

本專案為課程作業練習，僅供學習用途。

---

## 👤 作者

- **GitHub**: [soaring0616](https://github.com/soaring0616)
- **專案**: [mosaic_opencv](https://github.com/soaring0616/mosaic_opencv)

---

## 💡 延伸練習

- [ ] 實作 Hw4 完整版（使用邊緣特徵匹配小圖）
- [ ] 加入 GUI 即時調整參數
- [ ] 支援影片逐幀處理
- [ ] 優化 K-D Tree 查詢效能
- [ ] 加入多執行緒加速運算