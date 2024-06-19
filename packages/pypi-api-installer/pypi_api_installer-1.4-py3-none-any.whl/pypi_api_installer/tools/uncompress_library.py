import tarfile, shutil
import os

def uncompress_library (tar_gz_file:str, dst_path:str):
    file_path = tar_gz_file
    
    try:
        tar = tarfile.open(file_path)
        tar.extractall(path=dst_path)
        tar.close()
    except:
        main_path_name = os.path.dirname(tar_gz_file)
        base_name = os.path.basename(tar_gz_file)
        base_name = str(base_name).replace(".tar.gz", ".zip")
        shutil.copy2(tar_gz_file, os.path.join(main_path_name, base_name))
        import zipfile
        with zipfile.ZipFile(os.path.join(main_path_name, base_name), 'r') as zip_ref:
            zip_ref.extractall(dst_path)
        
        os.remove(os.path.join(main_path_name, base_name))

    os.remove(tar_gz_file)

if __name__ == "__main__":
    uncompress_library(tar_gz_file="requests.tar.gz", dst_path="requests")