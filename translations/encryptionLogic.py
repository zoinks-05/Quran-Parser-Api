import zipfile
import os

def compress_files(src, dst="translations/data/compressed"):
    os.makedirs(dst, exist_ok=True)

    src_file = f"{src}.txt"  # actual file on disk
    filename = os.path.basename(src_file)
    zip_path = os.path.join(dst, f"{os.path.basename(src)}.zip")

    if not os.path.isfile(src_file):
        print(f"File {src_file} not found. Cannot compress.")
        return

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(src_file, arcname=filename)  # write correct file

    # remove the .txt after compressing
    os.remove(src_file)

def decompressfile(src, dst='translations/data'):
    os.makedirs(dst, exist_ok=True)  # ensure destination exists
    print("Attempting to decompress:", src)
    print("ZIP exists?", os.path.exists(src))

    with zipfile.ZipFile(src, 'r') as zipf:
        print("Files inside ZIP:", zipf.namelist())
        zipf.extractall(dst)

def compress_all():
    src_dir = 'translations/data/ready/'
    dst_dir = 'translations/data/compressed/'

    for filename in os.listdir(src_dir):
        if filename.endswith('.txt'):
            src_path = os.path.join(src_dir, filename[:-4])
            compress_files(src_path, dst_dir)
            os.remove(os.path.join(src_dir, filename))

compress_all()


