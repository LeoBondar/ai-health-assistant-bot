import json
import os
import re
import tempfile
import zipfile

import aiohttp

def extract_words(input: str) -> list[str]:
    pattern = r'\b[\w.-]+@[\w.-]+\.\w+\b|\b\w+\b'
    matches = re.findall(pattern, input)

    return matches

def extract_words_tab(input: str) -> list[str]:
    lines = input.splitlines()
    line_list = []
    for line in lines:
        if line.strip():
            line_list.append(line.strip())
    return line_list

async def download_and_extract_zip(url: str) -> list[str]:
    files = []
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status != 200:
                raise Exception(f"Failed to download zip: {resp.status}")
            with tempfile.NamedTemporaryFile(delete=False, suffix=".zip") as tmp_zip:
                tmp_zip.write(await resp.read())
                tmp_zip_path = tmp_zip.name

    with zipfile.ZipFile(tmp_zip_path, 'r') as zip_ref:
        extract_dir = tempfile.mkdtemp()
        zip_ref.extractall(extract_dir)
        for file_name in zip_ref.namelist():
            file_path = os.path.join(extract_dir, file_name)
            if os.path.isfile(file_path):
                files.append(file_path)
    os.remove(tmp_zip_path)
    return files
