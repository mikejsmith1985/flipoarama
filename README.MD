# FLIPORAMA – Simple Local Flipbook Sheet Printer

Turns a folder of photos (JPG, PNG, or iPhone HEIC) into print-ready PDF sheets for classic thumb-flip flipbooks.

## Features
- Drag-and-drop upload (thousands of files OK)
- Automatic skipping of macOS hidden `._*` junk files
- Sorting: EXIF date (recommended), filename, or file timestamp
- Landscape or portrait pages
- Fully adjustable grid with sliders: 2–8 columns, 2–7 rows → any frame aspect you want
- True center-crop – frames completely fill their cells, no letterboxing
- Live low-res preview of the first printed page
- One-click “Generate Flipbook” with progress bar (nothing runs until you press it)
- Multi-page 8.5×11 PDF at print-ready resolution
- Very low RAM usage – works fine on older laptops with 300–500 frames

## Requirements
Python 3.9+ (tested on 3.12) and a virtual environment (strongly recommended).

## Install & Run
```bash
cd FLIPORAMA
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
streamlit run app.py

**Current state summary**
- Fully working local Streamlit app – no cloud, no accounts, runs offline after pip install
- Handles iPhone HEIC natively, skips macOS junk files automatically
- True center-crop (no white bars), wide-frame friendly defaults (3×4 landscape = nice 16:9-ish frames)
- Live sliders for grid size + orientation, preview of first page, button-triggered generation with progress bar
- Low memory (streams frames one-by-one), tested with 288 HEIC files → ~30–50 sec on normal laptop
- Outputs clean multi-page 300 dpi-effective PDF ready to print, cut, staple on the short edge, flip

**New README.md – just replace your old one**

```markdown
# FLIPORAMA – Simple Local Flipbook Sheet Printer

Turns a folder of photos (JPG, PNG, or iPhone HEIC) into print-ready PDF sheets for classic thumb-flip flipbooks.

## Features
- Drag-and-drop upload (thousands of files OK)
- Automatic skipping of macOS hidden `._*` junk files
- Sorting: EXIF date (recommended), filename, or file timestamp
- Landscape or portrait pages
- Fully adjustable grid with sliders: 2–8 columns, 2–7 rows → any frame aspect you want
- True center-crop – frames completely fill their cells, no letterboxing
- Live low-res preview of the first printed page
- One-click “Generate Flipbook” with progress bar (nothing runs until you press it)
- Multi-page 8.5×11 PDF at print-ready resolution
- Very low RAM usage – works fine on older laptops with 300–500 frames

## Requirements
Python 3.9+ (tested on 3.12) and a virtual environment (strongly recommended).

## Install & Run
```bash
cd FLIPORAMA
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## requirements.txt (exact versions that work)
```
streamlit==1.38.0
Pillow==12.0.0
pillow-heif==1.1.1
reportlab==4.2.2
```

## How to use
1. Drop your image folder (or select all files) into the uploader
2. Tweak sort, orientation, columns/rows until the preview looks right
3. Click the big red “Generate Flipbook” button
4. Wait for the progress bar (20–60 sec for a few hundred frames)
5. Download the PDF, print double-sided if you want, cut, staple on the short edge, flip!

## Tips for best results
- Shoot your stop-motion in landscape orientation (landscape video → wide frames)
- Use 3 columns × 4 rows in landscape for big cinematic frames
- Use 5–6 columns × 4–5 rows for more frames per page if you have hundreds
- Print on normal paper, cut with a paper cutter, staple tightly – works great

No internet required after install, no tracking, no accounts. Just print and flip.

Enjoy! 🐻🍯
```
```