"""One-time migration of the ISFs committed in the repository to release assets,
same layout as linker.py. See MIGRATION_RELEASES.md in skraper.

  python3 banners/migrate_releases.py upload    # resumable, rerun until it says "done"
  python3 banners/migrate_releases.py upload --wait-rate-limit   # waits out rate limits instead of stopping
  python3 banners/migrate_releases.py verify    # every ISF is an uploaded asset of the same size
  python3 banners/migrate_releases.py banners   # banners_plain.json: paths -> asset URLs
  python3 banners/migrate_releases.py rearrange # after a release layout change, re-uploads to the new releases
  python3 banners/migrate_releases.py cleanup [--yes]   # lists (deletes) the releases nothing references

The token is GH_TOKEN, or else the one of "gh auth token".
"""
import argparse
import hashlib
import json
import os
import random
import re
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import OrderedDict
from pathlib import Path

import natsort

SCRIPT_DIRECTORY = Path(__file__).parent
PROJECT_DIRECTORY = SCRIPT_DIRECTORY.parent
BANNERS_FILE = PROJECT_DIRECTORY / "banners/banners_plain.json"
RELEASES_FILE = PROJECT_DIRECTORY / "banners/releases.json"
REPOSITORY = "Abyss-W4tcher/volatility3-symbols"
ASSETS_PER_RELEASE = 1000
API_URL = "https://api.github.com"
UPLOADS_URL = "https://uploads.github.com"
RELEASE_NOTES = "Volatility3 symbols, see banners/banners_plain.json"
# releases.json is written every WRITE_EVERY uploads. After a crash, the assets
# uploaded but not recorded are found back by their label, not uploaded again.
WRITE_EVERY = 50
# Minimum wait on a rate limit with --wait-rate-limit, in seconds
RATE_LIMIT_WAIT = 300


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


def base_tag(relative_path: str):
    # Same as linker.py: <Distro>/<arch>/<X.Y.Z>, distribution suffix dropped
    directories = relative_path.split("/")[:-1]
    if len(directories) > 2:
        directories[2] = directories[2].split("+")[0]
    tag = "isf-" + "-".join(directories[:3])
    if "rt" in directories[3:]:
        tag += "-rt"
    return tag


def in_release_of(url: str, tag: str):
    # The asset URL is in release <tag>, or in its continuation <tag>-<n>
    return re.fullmatch(re.escape(tag) + r"(-\d+)?", url.split("/")[-2]) is not None


def release_tag(relative_path: str, releases: dict):
    # Same as linker.py
    tag = base_tag(relative_path)
    used_tags = [url.split("/")[-2] for url in releases.values()]
    candidate, n = tag, 1
    while used_tags.count(candidate) >= ASSETS_PER_RELEASE:
        n += 1
        candidate = f"{tag}-{n}"
    return candidate


def github_token():
    token = os.environ.get("GH_TOKEN")
    if not token:
        token = subprocess.run(["gh", "auth", "token"], capture_output=True, text=True).stdout.strip()
    if not token:
        # gh older than 2.17 has no "auth token"
        status = subprocess.run(
            ["gh", "auth", "status", "--hostname", "github.com", "--show-token"], capture_output=True, text=True
        )
        match = re.search(r"Token: (\S+)", status.stdout + status.stderr)
        token = match.group(1) if match else None
    if not token:
        sys.exit("No GitHub token: set GH_TOKEN, or log in with gh auth login")
    return token


class NoRedirect(urllib.request.HTTPRedirectHandler):
    # urllib keeps the Authorization header on redirects, whatever the host: a
    # redirect is returned as an HTTP error instead, the token is never sent on
    def redirect_request(self, *args, **kwargs):
        return None


API_OPENER = urllib.request.build_opener(NoRedirect)
VERBOSE = False


def debug(message):
    if VERBOSE:
        print(f"{time.strftime('%H:%M:%S')} {message}", flush=True)


def rate_limit_wait(headers):
    # At least RATE_LIMIT_WAIT, longer when GitHub says so
    wait = RATE_LIMIT_WAIT
    if headers.get("retry-after"):
        wait = max(wait, int(headers["retry-after"]) + 1)
    if headers.get("x-ratelimit-remaining") == "0":
        wait = max(wait, int(headers["x-ratelimit-reset"]) - int(time.time()) + 5)
    return wait


def request(method, url, data=None, content_type="application/json", attempts=10):
    """Returns (HTTP status, decoded JSON body). Retries server and network
    errors. On a rate limit, stops, or waits and retries without limit with
    --wait-rate-limit."""
    attempt = 0
    while True:
        headers = {
            "Authorization": f"Bearer {TOKEN}",
            "Accept": "application/vnd.github+json",
            "Content-Type": content_type,
        }
        start = time.time()
        try:
            with API_OPENER.open(urllib.request.Request(url, data, headers, method=method), timeout=600) as response:
                body = response.read()
                debug(f"{method} {url}: {response.status} in {time.time() - start:.1f}s")
                return response.status, json.loads(body) if body else None
        except urllib.error.HTTPError as e:
            body = e.read()
            debug(f"{method} {url}: {e.code} in {time.time() - start:.1f}s")
            if e.code in (403, 429) and (
                e.headers.get("retry-after") or e.headers.get("x-ratelimit-remaining") == "0" or b"rate limit" in body
            ):
                if not WAIT_RATE_LIMIT:
                    raise Exception(f"{method} {url}: rate limited, rerun later or with --wait-rate-limit")
                wait = rate_limit_wait(e.headers)
                print(f"{time.strftime('%H:%M:%S')} rate limited, waiting {wait}s", flush=True)
                time.sleep(wait)
                continue
            if e.code < 500:
                return e.code, json.loads(body) if body else None
            error = f"HTTP {e.code}"
        except (urllib.error.URLError, OSError) as e:
            error = str(e)
        attempt += 1
        if attempt == attempts:
            raise Exception(f"{method} {url}: still failing after {attempts} attempts, {error}")
        wait = min(2 ** (attempt - 1) * 5, 600)
        print(f"{method} {url}: {error}, retrying in {wait}s", flush=True)
        time.sleep(wait)


def release_id(tag: str, ids: dict):
    if tag not in ids:
        status, release = request("GET", f"{API_URL}/repos/{REPOSITORY}/releases/tags/{tag}")
        if status == 404:
            data = json.dumps({"tag_name": tag, "name": tag, "body": RELEASE_NOTES}).encode()
            status, release = request("POST", f"{API_URL}/repos/{REPOSITORY}/releases", data)
        if status not in (200, 201):
            raise Exception(f"Release {tag}: HTTP {status} {release}")
        ids[tag] = release["id"]
    return ids[tag]


def list_assets(release: int):
    assets, page = [], 1
    while True:
        status, response = request("GET", f"{API_URL}/repos/{REPOSITORY}/releases/{release}/assets?per_page=100&page={page}")
        if status != 200:
            raise Exception(f"Assets of release {release}: HTTP {status} {response}")
        if not response:
            return assets
        assets += response
        page += 1


def upload_asset(relative_path: str, releases: dict, ids: dict):
    tag = release_tag(relative_path, releases)
    release = release_id(tag, ids)
    data = (PROJECT_DIRECTORY / relative_path).read_bytes()
    debug(f"{relative_path}: {len(data)} bytes to {tag}")
    # The label is the relative path, as in linker.py. The second name is used
    # when another ISF of the release has the same asset name once renamed by
    # GitHub ("~" -> ".").
    names = [Path(relative_path).name, relative_path.replace("/", "_")]
    while True:
        query = urllib.parse.urlencode({"name": names[0], "label": relative_path})
        url = f"{UPLOADS_URL}/repos/{REPOSITORY}/releases/{release}/assets?{query}"
        status, asset = request("POST", url, data, "application/octet-stream")
        if status == 201:
            return asset["browser_download_url"]
        if status != 422:
            raise Exception(f"Upload of {relative_path} to {tag}: HTTP {status} {asset}")
        # The asset name is taken
        existing = [a for a in list_assets(release) if a["label"] == relative_path]
        if existing and existing[0]["state"] == "uploaded" and existing[0]["size"] == len(data):
            # Uploaded before a crash, not recorded
            debug(f"{relative_path}: already uploaded")
            return existing[0]["browser_download_url"]
        if existing:
            # Broken upload
            print(f"Deleting the broken asset of {relative_path} in {tag}", flush=True)
            status, response = request("DELETE", f"{API_URL}/repos/{REPOSITORY}/releases/assets/{existing[0]['id']}")
            if status != 204:
                raise Exception(f"Deleting asset {existing[0]['id']}: HTTP {status} {response}")
        elif len(names) > 1:
            names.pop(0)
            debug(f"{relative_path}: asset name taken by another ISF, uploading as {names[0]}")
        else:
            raise Exception(f"Upload of {relative_path} to {tag}: asset names taken {asset}")


def upload(delay: float):
    releases = load_releases()
    todo = natsort.natsorted(path for path in tracked_files() if path not in releases)
    print(f"{len(releases)} ISFs already in releases, {len(todo)} to upload", flush=True)
    ids, start = {}, time.time()
    try:
        for n, relative_path in enumerate(todo, 1):
            releases[relative_path] = upload_asset(relative_path, releases, ids)
            if n % WRITE_EVERY == 0:
                write_releases(releases)
                rate = n / (time.time() - start)
                print(f"{n}/{len(todo)} uploaded, {rate * 3600:.0f}/h, {(len(todo) - n) / rate / 3600:.1f}h left", flush=True)
            time.sleep(delay)
    finally:
        write_releases(releases)
    print("done", flush=True)


def verify(downloads: int):
    releases = load_releases()
    problems = [f"not in releases.json: {path}" for path in natsort.natsorted(tracked_files()) if path not in releases]
    by_tag = {}
    for path, url in releases.items():
        by_tag.setdefault(url.split("/")[-2], []).append(path)
    ids = {}
    for tag, paths in natsort.natsorted(by_tag.items()):
        assets = {a["label"]: a for a in list_assets(release_id(tag, ids))}
        for path in paths:
            asset = assets.get(path)
            local = PROJECT_DIRECTORY / path
            if not asset:
                problems.append(f"no asset labelled {path} in {tag}")
            elif asset["browser_download_url"] != releases[path] or asset["state"] != "uploaded":
                problems.append(f"{path}: {asset['state']} {asset['browser_download_url']}, releases.json has {releases[path]}")
            elif local.is_file() and asset["size"] != local.stat().st_size:
                problems.append(f"{path}: asset of {asset['size']} bytes, local file of {local.stat().st_size}")
            elif not in_release_of(releases[path], base_tag(path)):
                problems.append(f"{path}: in {tag}, not in {base_tag(path)}, run rearrange")
        print(f"{tag}: {len(paths)} checked", flush=True)
    # A few actual downloads, compared with the local files
    for path in random.sample(sorted(releases), min(downloads, len(releases))):
        local = PROJECT_DIRECTORY / path
        with urllib.request.urlopen(releases[path], timeout=600) as response:
            remote_hash = hashlib.sha256(response.read()).hexdigest()
        if local.is_file() and remote_hash != hashlib.sha256(local.read_bytes()).hexdigest():
            problems.append(f"{path}: downloaded content differs")
    print(f"{len(releases)} assets in {len(by_tag)} releases, {min(downloads, len(releases))} downloaded")
    for problem in problems:
        print(problem)
    if problems:
        sys.exit(f"{len(problems)} problems")
    print("ok")


def load_plain_banners():
    with open(BANNERS_FILE, "r") as f:
        return json.load(f)


def write_plain_banners(plain_banners: dict):
    with open(BANNERS_FILE, "w+") as f:
        f.write(json.dumps(OrderedDict(natsort.natsorted(plain_banners.items())), indent=1))


def banners():
    releases = load_releases()
    plain_banners = load_plain_banners()
    missing = []
    for banner, paths in plain_banners.items():
        missing += [path for path in paths if not path.startswith("https://") and path not in releases]
        plain_banners[banner] = [releases.get(path, path) for path in paths]
    if missing:
        sys.exit(f"{len(missing)} paths not in releases.json, banners not changed, e.g. {missing[:5]}")
    write_plain_banners(plain_banners)
    print("banners_plain.json written, now run banners/linker.py for banners.json")


def rearrange():
    """Re-uploads the assets that are not in their release any more (release
    layout change) to their release. The old releases are deleted by cleanup,
    once the new banners are published."""
    releases = load_releases()
    # The asset URLs of banners_plain.json (published by linker.py) go back to
    # their path, "banners" then writes the new URLs
    paths = {url: path for path, url in releases.items()}
    plain_banners = load_plain_banners()
    write_plain_banners({banner: [paths.get(entry, entry) for entry in entries] for banner, entries in plain_banners.items()})
    todo = natsort.natsorted(path for path, url in releases.items() if not in_release_of(url, base_tag(path)))
    print(f"{len(releases)} ISFs in releases, {len(todo)} to move", flush=True)
    ids, start = {}, time.time()
    try:
        for n, relative_path in enumerate(todo, 1):
            releases[relative_path] = upload_asset(relative_path, releases, ids)
            if n % WRITE_EVERY == 0:
                write_releases(releases)
                rate = n / (time.time() - start)
                print(f"{n}/{len(todo)} moved, {rate * 3600:.0f}/h, {(len(todo) - n) / rate / 3600:.1f}h left", flush=True)
    finally:
        write_releases(releases)
    print("done, now: banners, linker.py, commit and push the banners, then cleanup", flush=True)


def cleanup(delete: bool):
    """Deletes the isf-* releases, and their tags, that neither releases.json
    nor banners_plain.json reference."""
    used = {url.split("/")[-2] for url in load_releases().values()}
    for entries in load_plain_banners().values():
        used |= {entry.split("/")[-2] for entry in entries if entry.startswith("https://")}
    unused, page = [], 1
    while True:
        status, response = request("GET", f"{API_URL}/repos/{REPOSITORY}/releases?per_page=100&page={page}")
        if status != 200:
            raise Exception(f"Releases: HTTP {status} {response}")
        if not response:
            break
        unused += [r for r in response if r["tag_name"].startswith("isf-") and r["tag_name"] not in used]
        page += 1
    for release in unused:
        print(f"{release['tag_name']}: {len(release['assets'])} assets")
    if not delete:
        print(f"{len(unused)} releases not referenced, rerun with --yes to delete them with their tag")
        return
    for release in unused:
        status, response = request("DELETE", f"{API_URL}/repos/{REPOSITORY}/releases/{release['id']}")
        if status != 204:
            raise Exception(f"Deleting release {release['tag_name']}: HTTP {status} {response}")
        tag = urllib.parse.quote(release["tag_name"], safe="")
        status, response = request("DELETE", f"{API_URL}/repos/{REPOSITORY}/git/refs/tags/{tag}")
        # 422: the tag is already gone
        if status not in (204, 422):
            raise Exception(f"Deleting tag {release['tag_name']}: HTTP {status} {response}")
        print(f"deleted {release['tag_name']}", flush=True)
    print(f"{len(unused)} releases deleted")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    subparsers = parser.add_subparsers(dest="command", required=True)
    api = argparse.ArgumentParser(add_help=False)
    api.add_argument(
        "--wait-rate-limit",
        action="store_true",
        help=f"on a rate limit, wait (at least {RATE_LIMIT_WAIT}s) and retry, as many times as needed, instead of stopping",
    )
    api.add_argument("--verbose", action="store_true", help="log every ISF and API request, with its duration")
    upload_parser = subparsers.add_parser("upload", parents=[api])
    upload_parser.add_argument("--delay", type=float, default=0, help="seconds between two uploads")
    verify_parser = subparsers.add_parser("verify", parents=[api])
    verify_parser.add_argument("--downloads", type=int, default=20, help="assets to download and compare")
    subparsers.add_parser("banners")
    subparsers.add_parser("rearrange", parents=[api])
    cleanup_parser = subparsers.add_parser("cleanup", parents=[api])
    cleanup_parser.add_argument("--yes", action="store_true", help="delete the releases listed, instead of only listing them")
    args = parser.parse_args()
    TOKEN = github_token() if args.command != "banners" else None
    WAIT_RATE_LIMIT = getattr(args, "wait_rate_limit", False)
    VERBOSE = getattr(args, "verbose", False)
    if args.command == "upload":
        upload(args.delay)
    elif args.command == "verify":
        verify(args.downloads)
    elif args.command == "rearrange":
        rearrange()
    elif args.command == "cleanup":
        cleanup(args.yes)
    else:
        banners()
