from pathlib import Path
import lzma
import json
from base64 import b64encode, b64decode 

SCRIPT_DIRECTORY = Path(__file__).parent
PROJECT_DIRECTORY = SCRIPT_DIRECTORY.parent
BANNERS_FILE = PROJECT_DIRECTORY / "banners/banners_plain.json"
BANNERS_VOL_FILE = PROJECT_DIRECTORY / "banners/banners.json"

def uncompress_and_load_json(file_path):
    with lzma.open(file_path, 'rb') as compressed_file:
        decompressed_content = compressed_file.read()
        json_content = json.loads(decompressed_content)
    return json_content

def load_banners():
    if (BANNERS_FILE).is_file():
        with open(BANNERS_FILE, 'r') as f:
            return json.load(f)
    else:
        return {}

def write_new_banner(new_banner:dict):
    content = json.dumps(load_banners() | new_banner)
    with open(BANNERS_FILE, 'w+') as f:
        f.write(content)


banners = load_banners()

for file_path in PROJECT_DIRECTORY.rglob("**/*.xz"):
    relative_path = file_path.relative_to(PROJECT_DIRECTORY).as_posix()
    if any(relative_path in path for path in banners.values()):
        continue 
    try:
        json_content = uncompress_and_load_json(file_path)
        b64_banner = json_content['symbols']['linux_banner']['constant_data']
        banner = b64decode(b64_banner).rstrip(b'\x00').decode().strip()

        # avoid conflicts
        if banners.get(banner):
            if banners[banner] != relative_path:
                print("Conflict : ", banner, relative_path, banners[banner])
                break

        new_banner = {banner:relative_path}
        write_new_banner(new_banner)
    except Exception as e:
        print(f'Error : {e}', file_path)


plain_banners = load_banners()
vol_banners = {}
vol_banners["version"] = 1
vol_banners["linux"] = {}

for banner, path in plain_banners.items():
    banner = banner.encode() + b"\x00\n"
    vol_banners["linux"][b64encode(banner).decode()] = [f"https://github.com/Abyss-W4tcher/volatility3-symbols/raw/master/{path}"]

vol_banners = json.dumps(vol_banners)
with open(BANNERS_VOL_FILE, 'w+') as f:
    f.write(vol_banners)