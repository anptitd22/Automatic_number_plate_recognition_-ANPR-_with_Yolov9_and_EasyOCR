import os
import shutil
import urllib.request
from roboflow import Roboflow

def main():
    HOME = os.getcwd()
    print(HOME)
    # urls = [
    #     "https://github.com/WongKinYiu/yolov9/releases/download/v0.1/yolov9-c.pt",
    #     "https://github.com/WongKinYiu/yolov9/releases/download/v0.1/yolov9-e.pt",
    #     "https://github.com/WongKinYiu/yolov9/releases/download/v0.1/gelan-c.pt",
    #     "https://github.com/WongKinYiu/yolov9/releases/download/v0.1/gelan-e.pt"
    # ]
    #
    # # Đường dẫn thư mục lưu file (HOME/weights)
    # save_dir = os.path.join(HOME, "weights")
    # os.makedirs(save_dir, exist_ok=True)
    #
    # # Tải từng file
    # for url in urls:
    #     filename = os.path.basename(url)
    #     file_path = os.path.join(save_dir, filename)
    #     print(f"Downloading {filename} to {file_path}...")
    #     urllib.request.urlretrieve(url, file_path)
    #
    # print("Download completed.")

    # # Đăng nhập với API key của bạn
    # rf = Roboflow(api_key="7jExBT2BlsqOWsNZxLeV")
    #
    # # Truy cập workspace và project
    # project = rf.workspace("roboflow-universe-projects").project("license-plate-recognition-rxg4e")
    #
    # # Chọn version
    # version = project.version(11)
    #
    # # Tải dataset về ở định dạng YOLOv9
    # dataset = version.download("yolov9")
    #
    # # In ra đường dẫn đã tải
    # src_path = dataset.location
    # dst_path = os.path.join(HOME, os.path.basename(src_path))
    # dst_path = os.path.join(HOME, os.path.basename(src_path))
    #
    # if src_path != dst_path:
    #     shutil.move(src_path, dst_path)
    #     print(f"Dataset moved to current directory: {dst_path}")
    # else:
    #     print(f"Dataset already in current directory: {dst_path}")



if __name__ == '__main__':
    main()
    print("end.0")
