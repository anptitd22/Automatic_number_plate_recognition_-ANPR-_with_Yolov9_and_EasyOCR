import os
import uuid
import subprocess
import sys
import time
from fastapi import FastAPI, Request, UploadFile, File
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()
templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
app.mount("/result", StaticFiles(directory="result"), name="result")

os.makedirs("uploads", exist_ok=True)
os.makedirs("result", exist_ok=True)

def get_unique_filename(directory: str, filename: str) -> str:
    base, ext = os.path.splitext(filename)
    counter = 1
    new_name = filename
    while os.path.exists(os.path.join(directory, new_name)):
        new_name = f"{base}({counter}){ext}"
        counter += 1
    return new_name

def get_latest_exp_dir(base_path: str) -> str:
    """
    Trả về đường dẫn đầy đủ của thư mục exp mới nhất (vd: yolov9/runs/detect/exp4)
    """
    exp_dirs = [d for d in os.listdir(base_path) if d.startswith("exp")]
    if not exp_dirs:
        return None
    exp_dirs.sort(key=lambda d: os.path.getmtime(os.path.join(base_path, d)), reverse=True)
    return os.path.join(base_path, exp_dirs[0])

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/upload", response_class=HTMLResponse)
async def upload_video(request: Request, file: UploadFile = File(...)):
    start_time = time.time()

    allowed_extensions = {".mp4", ".avi", ".mov", ".mkv"}
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in allowed_extensions:
        return HTMLResponse(content="File format not supported.", status_code=400)

    # Lưu file tránh trùng tên
    filename = get_unique_filename("uploads", file.filename)
    upload_path = os.path.join("uploads", filename)
    with open(upload_path, "wb") as f:
        f.write(await file.read())

    # === Chạy YOLOv9 ===
    yolov9_cmd = [
        "python", "yolov9/anpromax.py",
        "--conf", "0.1",
        "--device", "cpu",
        "--weights", "yolov9/runs/train/exp/weights/best.pt",
        "--source", upload_path
    ]

    try:
        subprocess.run(yolov9_cmd, check=True)
    except subprocess.CalledProcessError as e:
        return HTMLResponse(content=f"YOLOv9 error: {e}", status_code=500)

    # === Tìm thư mục exp mới nhất sau khi YOLO chạy ===
    latest_exp_dir = get_latest_exp_dir("yolov9/runs/detect")
    if not latest_exp_dir:
        return HTMLResponse(content="Could not find YOLO output folder.", status_code=500)

    yolo_output_path = os.path.join(latest_exp_dir, filename)
    if not os.path.exists(yolo_output_path):
        return HTMLResponse(content=f"YOLO output file not found: {yolo_output_path}", status_code=500)

    # === Nén video lại với ffmpeg ===
    base_name, _ = os.path.splitext(filename)
    output_final_name = get_unique_filename("result", f"{base_name}_final.mp4")
    output_final_path = os.path.join("result", output_final_name)

    ffmpeg_cmd = [
        "ffmpeg", "-y",
        "-i", yolo_output_path,
        "-c:v", "libx264",
        output_final_path
    ]

    try:
        subprocess.run(ffmpeg_cmd, check=True)
    except subprocess.CalledProcessError as e:
        return HTMLResponse(content=f"FFmpeg error: {e}", status_code=500)

    # # === Mở file (nếu chạy local) ===
    # try:
    #     if os.name == "nt":
    #         os.startfile(output_final_path)
    #     elif os.name == "posix":
    #         subprocess.run(["open" if sys.platform == "darwin" else "xdg-open", output_final_path])
    # except Exception as e:
    #     print(f"Không thể mở video: {e}")

    end_time = time.time()
    processing_time = round(end_time - start_time, 2)

    return templates.TemplateResponse("index.html", {
        "request": request,
        "original": f"/uploads/{filename}",
        "result": f"/result/{output_final_name}",
        "processing_time": processing_time
    })
