# <img src="https://cdn-icons-png.flaticon.com/128/5088/5088992.png" width="3%" height="3%"> Volatility3 symbols

![](https://img.shields.io/badge/Symbols-8050-seagreen?style=flat-square)

![](https://img.shields.io/badge/Ubuntu-amd64%20|%20i386-dodgerblue?labelColor=lightsteelblue&style=for-the-badge&logo=ubuntu)  
![](https://img.shields.io/badge/Debian-amd64-darkcyan?labelColor=lightsteelblue&style=for-the-badge&logo=debian)  
![](https://img.shields.io/badge/KaliLinux-amd64-dodgerblue?labelColor=lightsteelblue&style=for-the-badge&logo=kalilinux)  
![](https://img.shields.io/badge/AlmaLinux-x86__64-darkcyan?labelColor=lightsteelblue&style=for-the-badge&logo=almalinux)  
![](https://img.shields.io/badge/RockyLinux-x86__64-dodgerblue?labelColor=lightsteelblue&style=for-the-badge&logo=rockylinux)  
![](https://img.shields.io/badge/macOS-amd64%20|%20i386-darkcyan?labelColor=lightsteelblue&style=for-the-badge&logo=macos)  

##❗27/03/25

Most of the macOS symbols for > 11.0 are not correct due to the use of incomplete KDKs. While a fix is developed, please be aware that analysis with these ISFs might be broken with Volatility3.

## Volatility3 memory analysis 🔍

Conducting memory analysis with Volatility3 against a Linux or macOS RAM capture, requires of an investigator to acquire appropriate kernel debugging information. 
As a compiled kernel produces a unique copy of this data, it can sometimes be tedious to access, manipulate, and transform it into the universal JSON **I**ntermediate **S**ymbol **F**ile format (required by Volatility3).

To save time, CPU, and bandwidth across the world, this repository contains a collection of ISF, generated from kernel sources of the most popular distributions.

## Usage

Place every compressed symbol file you plan to use inside your `<volatility3_installation>/volatility3/symbols/linux/` directory (create it if it doesn't exist).

Explore the `banners/banners_plain.json` file to match banners and symbols quickly, or navigate manually through the directories using the GitHub UI. <img src="https://cdn-icons-png.flaticon.com/128/5044/5044729.png" width="3%" height="3%">

### Practical example

After receiving a memory sample to analyze, we need to determine the kernel version and OS running on the machine at capture time :

```console
forensic-machine@analyst:~$ python3 vol.py -r pretty -f sample.bin banners
  |    Offset |                                                                                                                            Banner
* | 0x1400070 | Linux version 3.2.0-4-amd64 (debian-kernel@lists.debian.org) (gcc version 4.6.3 (Debian 4.6.3-14) ) #1 SMP Debian 3.2.57-3+deb7u2
```

We identified a Linux Debian kernel, and thanks to the `Linux banner`, we can search in this repository if the ISF was already generated. To do so, we can grab the `banners_plain.json` mapping file :

```console
forensic-machine@analyst:~$ wget https://raw.githubusercontent.com/Abyss-W4tcher/volatility3-symbols/master/banners/banners_plain.json
forensic-machine@analyst:~$ grep -A 2 'Linux version 3.2.0-4-amd64 (debian-kernel@lists.debian.org) (gcc version 4.6.3 (Debian 4.6.3-14) ) #1 SMP Debian 3.2.57-3+deb7u2' banners_plain.json

"Linux version 3.2.0-4-amd64 (debian-kernel@lists.debian.org) (gcc version 4.6.3 (Debian 4.6.3-14) ) #1 SMP Debian 3.2.57-3+deb7u2": [
  "Debian/amd64/3.2.0/4/Debian_3.2.0-4-amd64_3.2.57-3+deb7u2_amd64.json.xz"
 ],
```

We've got a match 🚀 ! Now, we can easily download the appropriate ISF directly in the Volatility3 symbols directory : 

```console
# Create <volatility3_installation>/volatility3/symbols/linux/ beforehand if it doesn't exist
forensic-machine@analyst:~$ wget https://github.com/Abyss-W4tcher/volatility3-symbols/raw/master/Debian/amd64/3.2.0/4/Debian_3.2.0-4-amd64_3.2.57-3+deb7u2_amd64.json.xz -P <volatility3_installation>/volatility3/symbols/linux/
```

The setup is now ready for memory analysis.

---

If you didn't get any match, please refer to the FAQ or the [Volatility3 documentation](https://volatility3.readthedocs.io/en/latest/symbol-tables.html#mac-or-linux-symbol-tables) to help you generate the ISF manually. 🦾

## Format

| Distribution | Path | Symbols | Example |
| ------------ | ---- | ------- | ------- |
| Ubuntu       | Ubuntu/<*architecture*>/<*base-kernel-version*>/<*ABI*>/<*kernel-flavour*>/ | Ubuntu\_<*kernel-version*>\_<*package-revision*>\_<*architecture*>.json.xz | Ubuntu/amd64/4.4.0/22/generic/Ubuntu\_4.4.0-22-generic\_4.4.0-22.40~14.04.1\_amd64.json.xz |
| Debian       | Debian/<*architecture*>/<*base-kernel-version*>/<*ABI*>/<*kernel-flavour*>/ | Debian\_<*kernel-version*>\_<*package-revision*>\_<*architecture*>.json.xz | Debian/amd64/3.1.0/1/Debian\_3.1.0-1-amd64\_3.1.1-1\_amd64.json.xz |
| KaliLinux       | KaliLinux/<*architecture*>/<*base-kernel-version*>/<*kernel-flavour*>/ | KaliLinux\_<*kernel-version*>\_<*package-revision*>\_<*architecture*>.json.xz | KaliLinux/amd64/5.2.0/KaliLinux\_5.2.0-kali2-amd64\_5.2.9-2kali1\_amd64.json.xz |
| AlmaLinux       | AlmaLinux/<*architecture*>/<*base-kernel-version*>/<*kernel-flavour*>/ | AlmaLinux\_<*kernel-version*>\_<*architecture*>.json.xz | AlmaLinux/x86\_64/4.18.0/AlmaLinux\_4.18.0-477.13.1.el8\_8\_x86\_64.json.xz |
| RockyLinux       | RockyLinux/<*architecture*>/<*base-kernel-version*>/<*kernel-flavour*>/ | RockyLinux\_<*kernel-version*>\_<*architecture*>.json.xz | RockyLinux/x86\_64/4.18.0/RockyLinux\_4.18.0-477.10.1.el8\_8\_x86\_64.json.xz |
| macOS       | macOS/<*version-prefixed*>/ | macOS\_KDK\_<*macOS-version*>\_build-<*build*>\_<*arch-if-mach-kernel*>.json.xz | macOS/14.0/macOS\_KDK\_14.0\_build-23A5257q.json.xz |

## FAQ

- *Some distributions are missing, do you plan to add them anytime soon ?*

Adding a new distribution is not particularly an issue, and I'd like to include as much as I can. However, I do not want to push the repository size too far, to avoid a potential removal by GitHub.

- *I can't find a specific kernel release in your repository, is there a way to generate the ISF manually ?*

Depending on the release policy of a kernel vendor, some versions might be considered "experimental" or "unstable", hence never making it to the "official" debug repositories (or at least not for a long time).

Take a look at the `symbols_finders/` directory, to help you find kernel packages not available in this repository or in the classic editor sources.

## macOS

Kernel debug symbols for macOS are fetched from : https://developer.apple.com/download/all. However, as Apple does not provide every build, some versions aren't available in this repository.
Here are some discussions about it :

- https://github.com/volatilityfoundation/volatility3/issues/155
- https://github.com/volatilityfoundation/volatility3/issues/541

## Fetching symbols automatically

Volatility3 provides a new feature allowing users to specify a remote ISF source to be queried when analyzing a memory dump. To test this feature in your local installation, add the following argument :

```sh
python3 vol.py --remote-isf-url 'https://github.com/Abyss-W4tcher/volatility3-symbols/raw/master/banners/banners.json' -f <memory_dump> <plugin>
```

## Related work 

A similar project for Volatility2 profiles is available here : https://github.com/Abyss-W4tcher/volatility2-profiles

EZ Volatility install script : https://github.com/Abyss-W4tcher/volatility-scripts/tree/master/vol_ez_install
