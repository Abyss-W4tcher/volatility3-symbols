from pathlib import Path
import lzma
import json
from base64 import b64encode, b64decode
import logging 

SCRIPT_DIRECTORY = Path(__file__).parent
PROJECT_DIRECTORY = SCRIPT_DIRECTORY.parent
BANNERS_FILE = PROJECT_DIRECTORY / "banners/banners_plain.json"
BANNERS_VOL_FILE = PROJECT_DIRECTORY / "banners/banners.json"


def uncompress_and_load_json(file_path):
    with lzma.open(file_path, "rb") as compressed_file:
        decompressed_content = compressed_file.read()
        json_content = json.loads(decompressed_content)
    return json_content


def load_banners():
    if (BANNERS_FILE).is_file():
        with open(BANNERS_FILE, "r") as f:
            return json.load(f)
    else:
        return {}


def write_new_banner(banners: dict):
    content = json.dumps(banners)
    with open(BANNERS_FILE, "w+") as f:
        f.write(content)


banners = load_banners()
banners_as_str = json.dumps(banners)

for file_path in PROJECT_DIRECTORY.rglob("**/*.xz"):
    relative_path = file_path.relative_to(PROJECT_DIRECTORY).as_posix()
    if relative_path in banners_as_str:
        continue

    try:
        json_content = uncompress_and_load_json(file_path)
        if relative_path.startswith("macOS"):
            b64_banner = json_content["symbols"]["version"]["constant_data"]
        else:
            b64_banner = json_content["symbols"]["linux_banner"]["constant_data"]

        banner = b64decode(b64_banner).rstrip(b"\x00").decode().strip()

        if banners.get(banner):
            banner_path = banners[banner]
            banner_path.append(relative_path)
        else:
            banner_path = [relative_path]

        banners = banners | {banner: banner_path}
        write_new_banner(banners)
        banners_as_str = json.dumps(banners)
    except Exception as e:
        logging.exception(f"Error computing {file_path}: {e}")

plain_banners = load_banners()
vol_banners = {}
vol_banners["version"] = 1
vol_banners["linux"] = {}
vol_banners["mac"] = {}

for banner, paths in plain_banners.items():
    banner = banner.encode() + b"\x00\n"
    paths_out = []

    for path in paths:
        key = "mac" if path.startswith("macOS") else "linux"
        paths_out.append(f"https://github.com/Abyss-W4tcher/volatility3-symbols/raw/master/{path}")

    vol_banners[key][b64encode(banner).decode()] = paths_out 

vol_banners = json.dumps(vol_banners)
with open(BANNERS_VOL_FILE, "w+") as f:
    f.write(vol_banners)
