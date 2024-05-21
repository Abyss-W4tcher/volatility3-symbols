import requests
from sys import argv
import re

BASE = "https://launchpad.net/ubuntu/{release}/{arch}/linux-image-unsigned-{version_short}-dbgsym/{version_extended}"
BASE2 = "https://launchpad.net/ubuntu/{release}/{arch}/linux-image-{version_short}-dbgsym/{version_extended}"


def get_ubuntu_releases():
    # https://lists.ubuntu.com/archives/ubuntu-release/2019-April/004757.html
    r = requests.get("https://api.launchpad.net/devel/ubuntu/series").json()
    releases = []
    for key in r["entries"]:
        releases.append(key["name"])
    return releases


def banner_infos(banner: str):
    try:
        version_short, version_extended = re.findall(
            "Linux version (\\d+\\.\\d+\\.\\d+-\\d+-\\S+).+\\(Ubuntu (\\d+\\.\\d+\\.\\d+-\\d+.\\S+)-\\S+.+\\)$",
            banner,
        )[0]
        if "amd64" in banner:
            arch = "amd64"
        elif "arm64" in banner:
            arch = "arm64"
        else:
            arch = "i386"
    except:
        print(
            'Cannot parse banner, verify its validity, by running the "banners" Volatility3 plugin.'
        )
        exit(1)

    return version_short, version_extended, arch


def search_debug_symbols(version_short, version_extended, arch) -> str:
    releases = get_ubuntu_releases()
    for base in [BASE, BASE2]:
        for release in releases:
            check = base.format(
                arch=arch,
                release=release,
                version_short=version_short,
                version_extended=version_extended,
            )
            r = requests.get(check)
            if r.status_code == 200:
                try:
                    download_url = re.findall(
                        f'href="(http://launchpadlibrarian\\.net/\\S+_{version_extended}_{arch}\\.ddeb)"',
                        r.text,
                    )[0]
                except:
                    print(
                        f"Detected URL {check} but download link couldn't be extracted."
                    )
                return download_url
    else:
        print("Couldn't find debug symbols.")
        exit(1)


def main():
    if len(argv) < 2:
        print(
            "Usage : python3 ubuntu_symbols_finder.py '[linux_banner]'. Example :\npython3 ubuntu_symbol_finder.py 'Linux version 5.15.0-43-generic (buildd@lcy02-amd64-076) (gcc (Ubuntu 11.2.0-19ubuntu1) 11.2.0, GNU ld (GNU Binutils for Ubuntu) 2.38) #46-Ubuntu SMP Tue Jul 12 10:30:17 UTC 2022 (Ubuntu 5.15.0-43.46-generic 5.15.39)'"
        )
        exit(1)

    banner = argv[1]
    version_short, version_extended, arch = banner_infos(banner)
    download_url = search_debug_symbols(version_short, version_extended, arch)

    ddeb_filename = download_url.split("/")[-1]
    ddeb_filename_without_extension = ddeb_filename.rsplit(".", 1)[0]
    procedure = f"""
wget {download_url}
dpkg-deb -x {ddeb_filename} {ddeb_filename_without_extension}/
dwarf2json linux --elf {ddeb_filename_without_extension}/usr/lib/debug/boot/{version_short} | xz > {ddeb_filename_without_extension}.json.xz"""
    print(
        f"Debug symbols should be available at {download_url}. Here is a typical procedure to create the ISF :\n{procedure}"
    )


if __name__ == "__main__":
    main()
