"""
ebook_to_pdf.py
スクリーンショット → PDF 変換スクリプト
主に印刷不可能な授業レジュメをPDFにするために作成。
使用は自己責任。

【必要ライブラリのインストール】
  python -m pip install pyautogui pillow img2pdf

【使い方】
  1. ターミナルで `python ebook_to_pdf.py` を実行
  2. カウントダウン中に被写体を前面に表示する
  3. 自動でスクリーンショット＆ページめくりを繰り返す
  4. 終わったら ebook_output.pdf が同じフォルダに生成される
  ※ 撮影した画像は screenshots フォルダにも保存されます
"""

import time
import os
import img2pdf
import pyautogui
from PIL import Image

# ===================== CONFIG =====================
TOTAL_PAGES       = 713         # 撮影するページ数
DELAY_BETWEEN     = 0.5           # ページめくり後の待機秒数
COUNTDOWN_SECONDS = 3           # 開始前のカウントダウン秒数
PAGE_TURN_KEY     = "right"     # ページめくりキー
OUTPUT_FILENAME   = "ebook_output.pdf"  # 出力PDFファイル名
SCREENSHOT_DIR    = "screenshots"       # 画像保存フォルダ名

# スクリーンショットの切り取り範囲（None で全画面）
# 例: (100, 50, 1300, 900)  → (left, top, right, bottom) ピクセル
CROP_REGION = None
# =================================================


def countdown(seconds: int):
    print(f"\n{'='*40}")
    print(f"  {seconds}秒後に開始します")
    print(f"  電子書籍アプリを前面にしてください！")
    print(f"{'='*40}")
    for i in range(seconds, 0, -1):
        print(f"  {i}...")
        time.sleep(1)
    print("  📸 スタート！\n")


def take_screenshot(page_num: int, save_dir: str) -> str:
    screenshot = pyautogui.screenshot()
    if CROP_REGION:
        screenshot = screenshot.crop(CROP_REGION)
    path = os.path.join(save_dir, f"{page_num:04d}.jpg")
    screenshot.convert("RGB").save(path, "JPEG", quality=95)
    print(f"  Page {page_num:>3} / {TOTAL_PAGES} 撮影完了")
    return path


def save_as_pdf(image_paths: list[str], output_path: str):
    print(f"\n📄 PDF を生成中... ({len(image_paths)} ページ)")
    with open(output_path, "wb") as f:
        f.write(img2pdf.convert(image_paths))
    size_mb = os.path.getsize(output_path) / 1024 / 1024
    print(f"✅ 完成！ → {output_path}  ({size_mb:.1f} MB)")


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    save_dir = os.path.join(script_dir, SCREENSHOT_DIR)
    os.makedirs(save_dir, exist_ok=True)

    print("\n🔖 ebook_to_pdf.py")
    print(f"   ページ数: {TOTAL_PAGES}")
    print(f"   ページめくりキー: {PAGE_TURN_KEY}")
    print(f"   待機時間: {DELAY_BETWEEN}秒 / ページ")
    print(f"   画像保存先: {save_dir}")

    countdown(COUNTDOWN_SECONDS)

    image_paths = []
    for page in range(1, TOTAL_PAGES + 1):
        path = take_screenshot(page, save_dir)
        image_paths.append(path)

        if page < TOTAL_PAGES:
            pyautogui.press(PAGE_TURN_KEY)
            time.sleep(DELAY_BETWEEN)

    output_path = os.path.join(script_dir, OUTPUT_FILENAME)
    save_as_pdf(image_paths, output_path)

    input("\nEnterキーで終了...")


if __name__ == "__main__":
    main()
