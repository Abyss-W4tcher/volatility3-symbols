from pathlib import Path
import lzma
import json
from base64 import b64encode, b64decode
import logging
import natsort
import subprocess
from collections import OrderedDict

SCRIPT_DIRECTORY = Path(__file__).parent
PROJECT_DIRECTORY = SCRIPT_DIRECTORY.parent
BANNERS_FILE = PROJECT_DIRECTORY / "banners/banners_plain.json"
BANNERS_VOL_FILE = PROJECT_DIRECTORY / "banners/banners.json"
# {relative path: release asset URL} of the ISFs published as release assets
RELEASES_FILE = PROJECT_DIRECTORY / "banners/releases.json"
REPOSITORY = "Abyss-W4tcher/volatility3-symbols"
ASSETS_PER_RELEASE = 1000


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


def write_new_banner(banners: dict, natsorted=False):
    if natsorted:
        content = json.dumps(OrderedDict(natsort.natsorted(banners.items())), indent=1)
    else:
        content = json.dumps(banners)
    with open(f"{BANNERS_FILE}", "w+") as f:
        f.write(content)


# ISFs committed before the switch to releases stay in the repository, at the
# same path. New ones are not committed (see .gitignore), but uploaded as
# release assets, and the banners point to their asset URL.


def load_releases():
    if RELEASES_FILE.is_file():
        with open(RELEASES_FILE, "r") as f:
            return json.load(f)
    return {}


def write_releases(releases: dict):
    with open(RELEASES_FILE, "w+") as f:
        f.write(json.dumps(OrderedDict(natsort.natsorted(releases.items())), indent=1))


def tracked_files():
    output = subprocess.run(
        ["git", "ls-files", "-z", "--", "*.xz"],
        cwd=PROJECT_DIRECTORY,
        capture_output=True,
        check=True,
        text=True,
    ).stdout
    return set(filter(None, output.split("\0")))


def gh(*args):
    return subprocess.run(
        ["gh", *args, "--repo", REPOSITORY],
        cwd=PROJECT_DIRECTORY,
        capture_output=True,
        check=True,
        text=True,
    ).stdout


def release_tag(relative_path: str, releases: dict):
    # One release per <Distro>/<arch>/<X.Y.Z>, the distribution suffix of the
    # base version directory dropped (Debian "6.12.33+deb13", "+bpo", Kali
    # "+kali"). rt kernels apart, as their file names are the same as the
    # standard ones (Alma/Rocky el9+). Releases are continued in <tag>-2,
    # <tag>-3... when full.
    directories = relative_path.split("/")[:-1]
    if len(directories) > 2:
        directories[2] = directories[2].split("+")[0]
    tag = "isf-" + "-".join(directories[:3])
    if "rt" in directories[3:]:
        tag += "-rt"
    used_tags = [url.split("/")[-2] for url in releases.values()]
    candidate, n = tag, 1
    while used_tags.count(candidate) >= ASSETS_PER_RELEASE:
        n += 1
        candidate = f"{tag}-{n}"
    return candidate


def gh_api(*args):
    return subprocess.run(
        ["gh", "api", *args],
        cwd=PROJECT_DIRECTORY,
        capture_output=True,
        check=True,
        text=True,
    ).stdout


def release_asset_url(tag: str, relative_path: str):
    # The asset label is its relative path: unique, and kept as is by GitHub
    # (asset names may be renamed). Assets are listed page by page, as a
    # release holds up to ASSETS_PER_RELEASE of them. An upload broken halfway
    # leaves an asset in another state, never returned: the next upload then
    # fails on its name, to be deleted by hand.
    release_id = gh_api(f"repos/{REPOSITORY}/releases/tags/{tag}", "--jq", ".id").strip()
    assets = gh_api(
        "--paginate",
        f"repos/{REPOSITORY}/releases/{release_id}/assets?per_page=100",
        "--jq",
        '.[] | select(.state == "uploaded") | .label + "\\t" + .browser_download_url',
    )
    for line in assets.splitlines():
        label, url = line.split("\t")
        if label == relative_path:
            return url
    return None


def upload(relative_path: str, releases: dict):
    tag = release_tag(relative_path, releases)
    try:
        url = release_asset_url(tag, relative_path)
    except subprocess.CalledProcessError:
        gh("release", "create", tag, "--title", tag, "--notes", "Volatility3 symbols, see banners/banners_plain.json")
        url = None
    if not url:
        # Never overwrites an asset (no --clobber) : an ISF is never rebuilt
        gh("release", "upload", tag, f"{PROJECT_DIRECTORY / relative_path}#{relative_path}")
        url = release_asset_url(tag, relative_path)
    if not url:
        raise Exception(f"Uploaded {relative_path} to {tag}, but cannot find the asset")
    # Recorded before the banners, so an asset is never uploaded twice
    releases[relative_path] = url
    write_releases(releases)
    return url


banners = load_banners()
banners_as_str = json.dumps(banners)
releases = load_releases()
tracked = tracked_files()

for file_path in PROJECT_DIRECTORY.rglob("**/*.xz"):
    relative_path = file_path.relative_to(PROJECT_DIRECTORY).as_posix()
    # Release asset first: the ISFs committed before the switch are migrated
    # to releases while still tracked (migrate_releases.py)
    entry = releases.get(relative_path)
    if not entry and relative_path in tracked:
        entry = relative_path
    if entry and entry in banners_as_str:
        continue

    try:
        json_content = uncompress_and_load_json(file_path)
        if relative_path.startswith("macOS"):
            b64_banner = json_content["symbols"]["version"]["constant_data"]
        else:
            b64_banner = json_content["symbols"]["linux_banner"]["constant_data"]

        banner = b64decode(b64_banner).rstrip(b"\x00").decode().strip()

        if not entry:
            entry = upload(relative_path, releases)

        if banners.get(banner):
            banner_path = banners[banner]
            banner_path.append(entry)
        else:
            banner_path = [entry]

        banners = banners | {banner: banner_path}
        write_new_banner(banners)
        banners_as_str = json.dumps(banners)
    except Exception as e:
        logging.exception(f"Error computing {file_path}: {e}")
        raise Exception("exit...")

write_new_banner(banners, natsorted=True)
plain_banners = load_banners()
release_paths = {url: path for path, url in releases.items()}
vol_banners = {}
vol_banners["version"] = 1
vol_banners["linux"] = {}
vol_banners["mac"] = {}

for banner, paths in plain_banners.items():
    banner = banner.encode() + b"\n\x00"
    paths_out = []

    for path in paths:
        key = "mac" if release_paths.get(path, path).startswith("macOS") else "linux"
        if path.startswith("https://"):
            # Release asset
            paths_out.append(path)
            continue
        paths_out.append(
            f"https://github.com/Abyss-W4tcher/volatility3-symbols/raw/master/{path}"
        )

    vol_banners[key][b64encode(banner).decode()] = paths_out

vol_banners = json.dumps(vol_banners, separators=(",", ":"))
with open(BANNERS_VOL_FILE, "w+") as f:
    f.write(vol_banners)
