# 【Blender】Colabでblendファイルをレンダリングする方法

> [!TIP]
> **狙い**
> Colabで `.blend` をレンダリングして、手元GPUが弱くても外部GPUで回せるようにする。

> [!NOTE]
> **このページでわかること**
> - Colabでのアップロード手順
> - Blenderのダウンロード・展開
> - GPUレンダリング（CYCLES / CUDA）
> - PNG → MP4 変換とダウンロード

## 📝 実行コード（Colabにそのままコピペして実行）

以下のブロックをColabのセルに貼り付けて、上から順に実行（または必要な部分を実行）してください。

```python
# ==========================================
# 0.1. GPU確認
# ==========================================
# ランタイムから「GPU」を選択し、認識されているか確認します。

!nvidia-smi

# ==========================================
# 0.2. ファイルをColabにアップロードする
# ==========================================

from google.colab import files
uploaded = files.upload()

# 🔎 メモ：アップロード後のパスはだいたい「 /content/ファイル名 」になります。
# ファイル名が分からないときは、別のセルで !ls を実行して確認してください。

# ==========================================
# 1. Blenderダウンロードと展開
# 🛠️ メモ：Blenderのバージョンは必要に応じて変更（URLと展開フォルダ名を揃える）
# ==========================================

!wget -nc [https://download.blender.org/release/Blender4.5/blender-4.5.6-linux-x64.tar.xz](https://download.blender.org/release/Blender4.5/blender-4.5.6-linux-x64.tar.xz)
!tar -xf blender-4.5.6-linux-x64.tar.xz

# ==========================================
# 2. blendファイルの指定
# ==========================================
# 📝 メモ：下の「ファイル名」を（0.2.）でアップロードしたものに書き換えてください

BLEND_FILE_PATH = "/content/ファイル名"
OUTPUT_DIR = "/content/render_output"
!mkdir -p "${OUTPUT_DIR}"

# ==========================================
# 3. GPUレンダリング（例：1〜100フレーム）
# 🛠️ メモ：CUDAが使えない環境では --cycles-device の指定を調整（環境依存）
# ==========================================

!./blender-4.5.6-linux-x64/blender -b "${BLEND_FILE_PATH}" \
  -E CYCLES \
  -o "${OUTPUT_DIR}/frame_#####" \
  -F PNG \
  -s 1 -e 100 -a -- --cycles-device CUDA

# ==========================================
# 4. PNG連番画像を 24fpsの高画質MP4 に変換する
# ==========================================

INPUT_DIR = "/content/render_output"
OUTPUT_FILE = "/content/final_movie_24fps.mp4"

!ffmpeg -y \
-framerate 24 \
-i {INPUT_DIR}/frame_%05d.png \
-c:v libx264 \
-preset slow \
-crf 18 \
-pix_fmt yuv420p \
-movflags +faststart \
{OUTPUT_FILE}

print("✅ 24fps動画 完成！")

# ==========================================
# 5. 完成したMP4をローカルにダウンロード
# ==========================================

from google.colab import files
files.download("/content/final_movie_24fps.mp4")

# ==========================================
# 🧾 まとめ
# ==========================================
# - 0.アップロード → 1.Blender展開 → 2.（0.2.）のファイルを指定 → 3.PNGレンダリング → 4.MP4化 → 5.ダウンロード
# - ↑の順にコピペして実行することで、google様の最高のGPUをお借りしてレンダリングが可能！
# - ノートPCでGPUが弱めの方、初心者で課金してレンダリングに手を出すのはちょっと……という方におすすめです。
# - 以上で終了です。ありがとうございました。
