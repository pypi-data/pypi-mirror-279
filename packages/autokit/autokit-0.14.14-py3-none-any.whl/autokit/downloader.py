import os
import shutil

import requests
import zipfile
import tempfile
from pathlib import Path


def download(tool_directory: Path, url: str, chunk_size=1024, progress_callback=None,
             file_type: str | None = None) -> None:
    """
    Downloads a file from the given URL and extracts it if it is a zip archive.

    :param tool_directory: The directory where the tool will be installed.
    :param url: The URL of the zip file.
    :param chunk_size: The size of the download chunks.
    :param progress_callback: A callback function to track the download progress.
    :param file_type: File type of the downloaded file. If None, the file type will be determined from the URL.
    """
    response = requests.get(url, stream=True)
    total_size_in_bytes = int(response.headers.get('content-length', 0))
    bytes_downloaded = 0

    # get the filename from the URL by splitting it at the last '/' and removing any query parameters
    filename = url.split('/')[-1].split('?')[0]

    file_suffix = "." + filename.split('.')[-1]

    if file_type is not None:
        file_suffix = file_type

    progress_context = type('', (), {})()

    with tempfile.NamedTemporaryFile(suffix=file_type, delete=False) as fp:
        temp_file_name = fp.name
        for chunk in response.iter_content(chunk_size=chunk_size):
            bytes_downloaded += len(chunk)
            fp.write(chunk)
            if progress_callback:
                progress_callback(progress_context, filename, bytes_downloaded, total_size_in_bytes)

    if progress_callback:
        progress_callback(progress_context, filename, total_size_in_bytes, total_size_in_bytes)

    if file_type or file_suffix == '.zip':
        with zipfile.ZipFile(temp_file_name, 'r') as zip_ref:
            zip_ref.extractall(tool_directory)
    else:
        shutil.copyfile(temp_file_name, tool_directory / filename)

    os.remove(temp_file_name)


