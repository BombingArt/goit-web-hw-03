from concurrent.futures import ThreadPoolExecutor, as_completed
import logging
import sys
import shutil
from pathlib import Path

def create_result_subdirectorys(path):
    extensions = ["jpeg", "jpg", "png", "svg"]
    for ext in extensions:
        subdirectory = path.joinpath(ext)
        if not subdirectory.exists():
            subdirectory.mkdir(parents=True, exist_ok=True)

def copy_files(file, target_dir):
    try:
        shutil.copy(file, target_dir)
        logging.info(f"Copied {file} to {target_dir}")
    except Exception as e:
        logging.warning(f"Error copying {file}: {e}")

def sort_by_extension(directory, copy_path):
    with ThreadPoolExecutor() as executor:
        futures = []
        for file in directory.iterdir():
            if file.is_dir():
                sort_by_extension(file, copy_path)
            else:
                extension = file.suffix.lower()
                if extension in [".jpeg", ".jpg", ".png", ".svg"]:
                    target_dir = copy_path.joinpath(extension[1:])
                    futures.append(executor.submit(copy_files, file, target_dir))
                else:
                    logging.warning(f"Unknown file extension: {extension}")
        for future in as_completed(futures):
            future.result()
                

def parse_args():
    directory_path = Path(sys.argv[1])
    
    if len(sys.argv) > 2:
        result_directory_path = Path(sys.argv[2])
    else:
        result_directory_path = Path("task_1/dist")

    return directory_path, result_directory_path
    
def main():
    directory_path, result_directory_path = parse_args()
    create_result_subdirectorys(result_directory_path)
    sort_by_extension(directory_path, result_directory_path)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
    main()