# <img src="https://cdn-icons-png.flaticon.com/128/5088/5088992.png" width="3%" height="3%"> Volatility3 symbols

![](https://img.shields.io/badge/Symbols-11712-seagreen?style=flat-square)

![](https://img.shields.io/badge/Ubuntu-amd64%20|%20i386-dodgerblue?labelColor=lightsteelblue&style=for-the-badge&logo=ubuntu)  
![](https://img.shields.io/badge/Debian-amd64-darkcyan?labelColor=lightsteelblue&style=for-the-badge&logo=debian)  
![](https://img.shields.io/badge/KaliLinux-amd64-dodgerblue?labelColor=lightsteelblue&style=for-the-badge&logo=kalilinux)  
![](https://img.shields.io/badge/AlmaLinux-x86__64-darkcyan?labelColor=lightsteelblue&style=for-the-badge&logo=almalinux)  
![](https://img.shields.io/badge/RockyLinux-x86__64-dodgerblue?labelColor=lightsteelblue&style=for-the-badge&logo=rockylinux)  
![](https://img.shields.io/badge/macOS-amd64%20|%20i386-darkcyan?labelColor=lightsteelblue&style=for-the-badge&logo=macos)  

## 10/20/2026 ISFs moved to GitHub Releases 📦

Their repository paths (`raw/master/<Distro>/...`) stop working on **11/21/2026**. Use `banners/banners.json` with Volatility3 `--remote-isf-url`, or `banners/banners_plain.json` in scripts: only these two URLs are stable, every ISF location is read from them and may change. If Volatility3 does not find a kernel after that date, run it once with `--clear-cache`. Behind a firewall allowlist, also allow `release-assets.githubusercontent.com`. The many releases created on 10/20/2026 and 10/21/2026 are this move, a one-time change.

## Volatility3 memory analysis 🔍

Conducting memory analysis with Volatility3 against a Linux or macOS RAM capture, requires of an investigator to acquire appropriate kernel debugging information. 
As a compiled kernel produces a unique copy of this data, it can sometimes be tedious to access, manipulate, and transform it into the universal JSON **I**ntermediate **S**ymbol **F**ile format (required by Volatility3).

To save time, CPU and bandwidth across the world, this repository contains a collection of ISFs generated from kernel sources of the most popular distributions.

## Usage

Volatility3 >= v2.11.0 with Internet access can query remote ISF indexes on its own and automatically try to find the appropriate ISF for you:

```sh
python3 vol.py --remote-isf-url 'https://github.com/Abyss-W4tcher/volatility3-symbols/raw/master/banners/banners.json' -f <memory_dump_path> <plugin>
```

If no match is found that means this repository does not have the correct ISF associated with the memory sample. You can refer to the FAQ or the [Volatility3 documentation](https://volatility3.readthedocs.io/en/latest/symbol-tables.html#mac-or-linux-symbol-tables) to help you generate the ISF manually.

### Practical example (without `--remote-isf-url`)

After receiving a memory sample to analyze, we need to determine the kernel version and OS running on the machine at capture time :

```console
forensic-machine@analyst:~$ python3 vol.py -r pretty -f sample.bin banners
  |    Offset |                                                                                                                            Banner
* | 0x1400070 | Linux version 3.2.0-4-amd64 (debian-kernel@lists.debian.org) (gcc version 4.6.3 (Debian 4.6.3-14) ) #1 SMP Debian 3.2.57-3+deb7u2
```

We identified a Linux Debian kernel, and thanks to the `Linux banner`, we can search the index for an ISF. To do so, we can grab the `banners_plain.json` mapping file :

```console
forensic-machine@analyst:~$ wget https://github.com/Abyss-W4tcher/volatility3-symbols/raw/master/banners/banners_plain.json
forensic-machine@analyst:~$ grep -A 2 'Linux version 3.2.0-4-amd64 (debian-kernel@lists.debian.org) (gcc version 4.6.3 (Debian 4.6.3-14) ) #1 SMP Debian 3.2.57-3+deb7u2' banners_plain.json

"Linux version 3.2.0-4-amd64 (debian-kernel@lists.debian.org) (gcc version 4.6.3 (Debian 4.6.3-14) ) #1 SMP Debian 3.2.57-3+deb7u2": [
  "https://github.com/Abyss-W4tcher/volatility3-symbols/releases/download/isf-Debian-amd64-3.2.0/Debian_3.2.0-4-amd64_3.2.57-3%2Bdeb7u2_amd64.json.xz"
 ],
```

We've got a match 🚀 ! Now, we can download this ISF directly in the Volatility3 symbols directory (its file name does not matter, Volatility3 reads the banner inside) :

```console
# Create <volatility3_installation>/volatility3/symbols/linux/ beforehand if it doesn't exist
forensic-machine@analyst:~$ wget 'https://github.com/Abyss-W4tcher/volatility3-symbols/releases/download/isf-Debian-amd64-3.2.0/Debian_3.2.0-4-amd64_3.2.57-3%2Bdeb7u2_amd64.json.xz' -P <volatility3_installation>/volatility3/symbols/linux/
```

The setup is now ready for memory analysis.

## FAQ

- *I can't find a specific kernel release in your repository, is there a way to generate the ISF manually ?*

Depending on the release policy of a kernel vendor, some versions might be considered "experimental" or "unstable", hence never making it to the "official" debug repositories (or at least not for a long time).

The `symbols_finders/` directory contains scripts and procedures to help analysts build ISFs not found in this directory (currently Ubuntu and Alpine).

## macOS

> [!WARNING]
> macOS analysis support is no longer actively maintained in Volatility3 since its parity release with Volatility2. The existing macOS plugins remain available, but may not receive future updates, see the [official announcement](https://volatilityfoundation.org/announcing-the-official-parity-release-of-volatility-3/#:~:text=the%20parity%20release.-,macOS,-Apple%20has%20made). The macOS symbols of this repository are kept for legacy samples.


Kernel debug symbols for macOS are fetched from : https://developer.apple.com/download/all. However, as Apple does not provide every build, some versions aren't available in this repository.
Here are some discussions about it :

- https://github.com/volatilityfoundation/volatility3/issues/155
- https://github.com/volatilityfoundation/volatility3/issues/541

**10/21/2026**: the symbols for macOS 11.0 and later were removed. Most of them were not correct, due to incomplete KDKs, and analysis with them could be broken with Volatility3. Symbols for macOS 10.x are still available.

