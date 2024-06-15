import os
import glob
import pandas as pd
from fastdup.definitions import *
from datetime import datetime
from fastdup.sentry import fastdup_capture_exception


def download_from_s3(input_dir, work_dir, verbose, is_test=False):
    """
    Download files from S3 to local disk (called only in case of turi_param='sync_s3_to_local=1')
    Note: we assume there is enough local disk space otherwise the download may fail
     input_dir: input directory on s3 or minio
     work_dir: local working directory
     verbose: if verbose show progress
     is_test: If this is a test folder save it on S3_TEST_TEMP_FOLDER otherwise on S3_TEMP_FOLDER
    Returns: The local download directory
    """
    print(f'Going to download s3 files from {input_dir} to local {work_dir}')

    local_folder = S3_TEST_TEMP_FOLDER if is_test else S3_TEMP_FOLDER
    if input_dir.startswith('s3://'):
        command = 'aws s3 sync ' + input_dir + ' ' + f'{work_dir}/{local_folder}'
        if not verbose:
            command += ' --no-progress'
        ret = os.system(command)
        if ret != 0:
            print('Failed to sync s3 to local. Command was aws s3 sync ' + input_dir + ' ' + f'{work_dir}/{local_folder}')
            return ret
    elif input_dir.startswith('minio://'):
        command = 'mc cp --recursive ' + input_dir.replace('minio://', '') + ' ' + f'{work_dir}/{local_folder} '
        if not verbose:
            command += ' --quiet'
        ret = os.system(command)
        if ret != 0:
            print('Failed to sync s3 to local. Command was: mc cp --recursive ' + input_dir.replace('minio://', '') + ' ' + f'{work_dir}/{local_folder}')
            return ret
    input_dir = f'{work_dir}/{local_folder}'
    return input_dir

def check_latest_version(curversion):
    try:
        import requests
        from packaging.version import parse

        # Search for the package on PyPI using the PyPI API
        response = requests.get('https://pypi.org/pypi/fastdup/json')

        # Get the latest version number from the API response
        latest_version = parse(response.json()['info']['version'])

        latest_version = (int)(float(str(latest_version))*1000)
        if latest_version > (int)(float(curversion)*1000)+10:
            return True

    except Exception as e:
        fastdup_capture_exception("check_latest_version", e, True)


    return False



def record_time():
    try:
        now = datetime.now()
        date_time = now.strftime("%Y-%m-%d")
        with open("/tmp/.timeinfo", "w") as f:
            if date_time.endswith('%'):
                date_time = date_time[:len(date_time)-1]
            f.write(date_time)
    except Exception as ex:
        fastdup_capture_exception("Timestamp", ex)



def get_images_from_path(path):
    "List a subfoler recursively and get all image files supported by fastdup"
    # create list to store results

    assert os.path.isdir(path), "Failed to find directory " + path
    filenames = []
    ret = []
    # get all image files
    image_extensions = SUPPORTED_IMG_FORMATS
    image_extensions.extend(SUPPORTED_VID_FORMATS)
    filenames += glob.glob(f'{path}/**/*', recursive=True)

    for r in filenames:
        ext = os.path.splitext(r)
        if len(ext) < 2:
            continue
        ext = ext[1]
        if ext in image_extensions:
            ret.append(r)

    if len(ret) == 0:
        print("Warning: failed to find any image/video files in folder " + path)
    return ret


def list_subfolders_from_file(file_path):
    assert os.path.isfile(file_path)
    ret = []

    with open(file_path, "r") as f:
        for line in f:
            if os.path.isdir(line.strip()):
               ret += get_images_from_path(line.strip())

    assert len(ret), "Failed to find any folder listing from file " + file_path
    return ret


def shorten_path(path):
    if path.startswith('./'):
        path = path[2:]

    if path.endswith('/'):
        path = path[:-1]

    cwd = os.getcwd()
    if (path.startswith(cwd + '/')):
        path = path.replace(cwd + '/', '')

    return path

def check_if_folder_list(file_path):
    assert os.path.isfile(file_path), "Failed to find file " + file_path
    if file_path.endswith('yaml'):
        return False
    with open(file_path, "r") as f:
        for line in f:
            return os.path.isdir(line.strip())
    return False

def save_as_csv_file_list(filenames, files_path):
     files = pd.DataFrame({'filename':filenames})
     files.to_csv(files_path)
     return files_path


def expand_list_to_files(the_list):
    assert len(the_list), "Got an emplty list for input"
    files = []
    for f in the_list:
        if f.startswith("s3://") or f.startswith("minio://"):
            assert False, "Unsupported mode: can not run on lists of s3 folders, please list all files in s3 and give a list of all files each one in a new row"
        if os.path.isfile(f):
            files.append(f)
        else:
            files.extend(get_images_from_path)
    assert len(files), "Failed to extract any files from list"
    return files

def ls_crop_folder(path):
    assert os.path.isdir(path), "Failed to find directlry " + path
    files = os.listdir(path)
    df = pd.DataFrame({'filename':files})
    assert len(df), "Failed to find any crops in folder " + path


if __name__ == "__main__":
    print(list_subfolders_from_file("file.txt"))