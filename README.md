# <img src="https://cdn-icons-png.flaticon.com/128/5088/5088992.png" width="3%" height="3%"> Volatility3 symbols

![](https://img.shields.io/badge/Symbols-6910-seagreen?style=flat-square)

![](https://img.shields.io/badge/Ubuntu-amd64%20|%20i386-dodgerblue?labelColor=lightsteelblue&style=for-the-badge&logo=ubuntu)  
![](https://img.shields.io/badge/Debian-amd64-darkcyan?labelColor=lightsteelblue&style=for-the-badge&logo=debian)  
![](https://img.shields.io/badge/KaliLinux-amd64-dodgerblue?labelColor=lightsteelblue&style=for-the-badge&logo=kalilinux)  
![](https://img.shields.io/badge/AlmaLinux-x86__64-darkcyan?labelColor=lightsteelblue&style=for-the-badge&logo=almalinux)  
![](https://img.shields.io/badge/RockyLinux-x86__64-dodgerblue?labelColor=lightsteelblue&style=for-the-badge&logo=rockylinux)  
![](https://img.shields.io/badge/macOS-amd64%20|%20i386-darkcyan?labelColor=lightsteelblue&style=for-the-badge&logo=macos)  

## Related work 

A similar project for Volatility2 profiles is available here : https://github.com/Abyss-W4tcher/volatility2-profiles

EZ Volatility install script : https://github.com/Abyss-W4tcher/volatility-scripts/tree/master/vol_ez_install

## Format

| Distribution | Path | Symbols | Example |
| ------------ | ---- | ------- | ------- |
| Ubuntu       | Ubuntu/<*architecture*>/<*base-kernel-version*>/<*ABI*>/<*kernel-flavour*>/ | Ubuntu\_<*kernel-version*>\_<*package-revision*>\_<*architecture*>.json.xz | Ubuntu/amd64/4.4.0/22/generic/Ubuntu\_4.4.0-22-generic\_4.4.0-22.40~14.04.1\_amd64.json.xz |
| Debian       | Debian/<*architecture*>/<*base-kernel-version*>/<*ABI*>/<*kernel-flavour*>/ | Debian\_<*kernel-version*>\_<*package-revision*>\_<*architecture*>.json.xz | Debian/amd64/3.1.0/1/Debian\_3.1.0-1-amd64\_3.1.1-1\_amd64.json.xz |
| KaliLinux       | KaliLinux/<*architecture*>/<*base-kernel-version*>/<*kernel-flavour*>/ | KaliLinux\_<*kernel-version*>\_<*package-revision*>\_<*architecture*>.json.xz | KaliLinux/amd64/5.2.0/KaliLinux\_5.2.0-kali2-amd64\_5.2.9-2kali1\_amd64.json.xz |
| AlmaLinux       | AlmaLinux/<*architecture*>/<*base-kernel-version*>/<*kernel-flavour*>/ | AlmaLinux\_<*kernel-version*>\_<*architecture*>.json.xz | AlmaLinux/x86\_64/4.18.0/AlmaLinux\_4.18.0-477.13.1.el8\_8\_x86\_64.json.xz |
| RockyLinux       | RockyLinux/<*architecture*>/<*base-kernel-version*>/<*kernel-flavour*>/ | RockyLinux\_<*kernel-version*>\_<*architecture*>.json.xz | RockyLinux/x86\_64/4.18.0/RockyLinux\_4.18.0-477.10.1.el8\_8\_x86\_64.json.xz |
| macOS       | macOS/<*version-prefixed*>/ | macOS\_KDK\_<*macOS-version*>\_build-<*build*>\_<*arch-if-mach-kernel*>.json.xz | macOS/14.0/macOS\_KDK\_14.0\_build-23A5257q.json.xz |

## Usage

Place every compressed symbol file you plan to use inside your `[volatility3_installation]/volatility3/symbols/linux/` directory (create it if needed).

Explore the "banners/banners_plain.json" file to match banners and symbols quickly.

## FAQ

- *Some distributions are missing, do you plan to add them anytime soon ?*

Adding a new distribution is not particularly an issue, and I'd like to include as much as I can. However, I do not want to push the repository size too far, to avoid a potential removal by GitHub.

- *Why can't I locate symbols for a particular subversion of a listed distribution ?*

    - Ubuntu :
        It appears that debug symbols for pre-release and test kernels aren't automatically generated along the kernel source code, in [Ubuntu ddebs mirror](http://ddebs.ubuntu.com/).
      You might want to take a look at the [Canonical Kernel Team](https://launchpad.net/~canonical-kernel-team/+archive/ubuntu/ppa) PPA, for non-stable kernels. Check out issue [#27](https://github.com/Abyss-W4tcher/volatility3-symbols/issues/27) for an example.
      
Due to missing dependencies, some kernels specific versions may not be available here. 

## macOS

Kernel debug symbols for macOS are fetched from : https://developer.apple.com/download/all. However, as Apple does not provide every build, some versions aren't available in this repository.
Here are some discussions about it :

- https://github.com/volatilityfoundation/volatility3/issues/155
- https://github.com/volatilityfoundation/volatility3/issues/541

## Fetching symbols automatically

Volatility3 provides a new feature allowing users to specify a remote symbols source to be queried when analyzing a memory dump. To test this feature in your local installation, run the following commands :

```sh
VOLATILITY3_PATH=/path/to/volatility3_install/ # Edit accordingly
sed -i 's@REMOTE_ISF_URL = None@REMOTE_ISF_URL = "https://github.com/Abyss-W4tcher/volatility3-symbols/raw/master/banners/banners.json"@g' "$VOLATILITY3_PATH/volatility3/framework/constants/__init__.py"
```
