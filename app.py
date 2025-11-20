import streamlit as st
from pathlib import Path
from PIL import Image
from pillow_heif import register_heif_opener
register_heif_opener()
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader
import io, tempfile, shutil

st.set_page_config(page_title="FLIPORAMA", layout="centered")
st.title("FLIPORAMA – Flipbook Sheet Maker")

# Session state
for key in ["uploaded_files", "pdf_bytes", "preview_img"]:
    if key not in st.session_state:
        st.session_state[key] = None

# ====================== UI ======================
uploaded_folder = st.file_uploader(
    "Drop a folder of images",
    type=['jpg','jpeg','png','heic','heif'],
    accept_multiple_files=True
)

if uploaded_folder:
    st.session_state.uploaded_files = uploaded_folder

    # Count only count real images for the message
    valid_files = [f for f in uploaded_folder if not f.name.startswith(('.','._'))]
    skipped = len(uploaded_folder) - len(valid_files)

    st.success(f"{len(valid_files)} valid images loaded"
               + (f" (skipped {skipped} hidden/macOS junk files)" if skipped else "")
               + " – adjust settings then click Generate")
else:
    st.info("Upload images to start")
    st.stop()

sort_key = st.selectbox(
    "Sort images by",
    ["EXIF DateTimeOriginal (recommended)", "Filename alphanumeric", "File modification time", "File creation time"],
    index=0
)

orientation = st.selectbox(
    "Page orientation",
    ["Landscape (recommended for wide frames)", "Portrait"],
    index=0
)

st.info("Wide frames → low columns + high rows    |    Tall frames → high columns + low rows")

col1, col2 = st.columns(2)
with col1:
    cols = st.slider("Columns", 2, 8, 3)
with col2:
    rows = st.slider("Rows", 2, 7, 4)

frames_per_page = rows * cols

if st.button("Generate Flipbook", type="primary"):
    if not st.session_state.uploaded_files:
        st.error("Upload images first")
        st.stop()

    with st.spinner("Processing images…"):
        temp_dir = tempfile.mkdtemp()
        images = []
        for f in st.session_state.uploaded_files:
            if f.name.startswith('._') or f.name.startswith('.'):
                continue
            path = Path(temp_dir) / f.name
            path.write_bytes(f.getvalue())
            images.append(path)

        if not images:
            st.stop()

        def get_sort_key(p):
            if sort_key == "EXIF DateTimeOriginal (recommended)":
                try:
                    img = Image.open(p)
                    exif = img.getexif()
                    if exif:
                        dt = exif.get(36867)
                        if dt:
                            return str(dt)
                except Exception:
                    pass
                return "9999:99:99 99:99:99"
            elif sort_key == "Filename alphanumeric":
                return p.name.lower()
            elif sort_key == "File modification time":
                return p.stat().st_mtime
            else:
                return p.stat().st_ctime

        images.sort(key=get_sort_key)

        pagesize = landscape(letter) if "Landscape" in orientation else letter
        page_w, page_h = pagesize

        margin = 0.25 * inch
        gutter = 0.1 * inch

        cell_w = (page_w - 2*margin - (cols - 1)*gutter) / cols
        cell_h = (page_h - 2*margin - (rows - 1)*gutter) / rows

        target_ratio = cell_w / cell_h

        def prepare_frame(img):
            img = img.convert("RGB")
            img_ratio = img.width / img.height

            if img_ratio < target_ratio:
                new_h = int(img.width / target_ratio)
                top = (img.height - new_h) // 2
                img = img.crop((0, top, img.width, top + new_h))
            else:
                new_w = int(img.height * target_ratio)
                left = (img.width - new_w) // 2
                img = img.crop((left, 0, left + new_w, img.height))

            return img.resize((int(cell_w), int(cell_h)), Image.LANCZOS)

        processed = [prepare_frame(Image.open(p)) for p in images]

        if processed:
            preview_size = (int(page_w // 1.5), int(page_h // 1.5))
            preview = Image.new("RGB", preview_size, "white")
            scale = 1.5

            for i in range(min(len(processed), frames_per_page)):
                row = i // cols
                col = i % cols
                frame = processed[i].resize((int(cell_w / scale), int(cell_h / scale)), Image.LANCZOS)

                x = int((margin / scale) + col * (cell_w + gutter) / scale)
                y = int((margin / scale) + row * (cell_h + gutter) / scale)
                preview.paste(frame, (x, y))

            st.session_state.preview_img = preview

        pdf_bytes = io.BytesIO()
        c = canvas.Canvas(pdf_bytes, pagesize=pagesize)
        c.setCreator("FLIPORAMA")

        for page_idx in range(0, len(processed), frames_per_page):
            if page_idx > 0:
                c.showPage()

            num_on_page = min(frames_per_page, len(processed) - page_idx)
            for i in range(num_on_page):
                row = i // cols
                col = i % cols

                x = margin + col * (cell_w + gutter)
                y = page_h - margin - cell_h - row * (cell_h + gutter)

                img_data = io.BytesIO()
                processed[page_idx + i].save(img_data, format="JPEG", quality=95)
                img_data.seek(0)

                c.drawImage(ImageReader(img_data), x, y, width=cell_w, height=cell_h)

        c.save()
        pdf_bytes.seek(0)

        st.session_state.pdf_bytes = pdf_bytes.getvalue()

        shutil.rmtree(temp_dir)

    st.success(f"Ready! {len(processed)} frames processed → {((len(processed)-1)//frames_per_page + 1)} pages")

if st.session_state.pdf_bytes:
    if st.session_state.preview_img:
        st.subheader("Preview – first page (low-res)")
        st.image(st.session_state.preview_img, use_container_width=True)

    st.download_button(
        "Download flipbook_print.pdf",
        st.session_state.pdf_bytes,
        "flipbook_print.pdf",
        "application/pdf"
    )

# =====================