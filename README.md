# <img src="https://cdn-icons-png.flaticon.com/128/5088/5088992.png" width="3%" height="3%"> Volatility3 symbols

![](https://img.shields.io/badge/Symbols-6462-seagreen?style=flat-square)

![](https://img.shields.io/badge/Ubuntu%20kernels/amd64-3.13.0%20--%3E%206.5.0-dodgerblue?labelColor=lightsteelblue&style=for-the-badge&logo=ubuntu)  
![](https://img.shields.io/badge/Ubuntu%20kernels/i386-3.13.0%20--%3E%205.4.0-darkcyan?labelColor=lightsteelblue&style=for-the-badge&logo=ubuntu)  
![](https://img.shields.io/badge/Debian%20kernels/amd64-2.6.32%20--%3E%206.4.0-dodgerblue?labelColor=lightsteelblue&style=for-the-badge&logo=debian)  
![](https://img.shields.io/badge/KaliLinux%20kernels/amd64-3.18.0%20--%3E%206.5.0-darkcyan?labelColor=lightsteelblue&style=for-the-badge&logo=kalilinux)  
![](https://img.shields.io/badge/AlmaLinux%20kernels/amd64-4.18.0%20%7C%205.14.0-dodgerblue?labelColor=lightsteelblue&style=for-the-badge&logo=almalinux)  
![](https://img.shields.io/badge/RockyLinux%20kernels/amd64-4.18.0%20%7C%205.14.0-darkcyan?labelColor=lightsteelblue&style=for-the-badge&logo=rockylinux)  
![](https://img.shields.io/badge/macOS%20versions-10.6.3%20--%3E%2014.0-dimgray?labelColor=lightsteelblue&style=for-the-badge&logo=macos) 

## Related work 

A similar project for Volatility2 profiles is available here : https://github.com/Abyss-W4tcher/volatility2-profiles

Generate your own Volatility3 symbols with : https://github.com/Abyss-W4tcher/volatility-scripts/tree/master/symbols_builder

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


## FAQ

- *Why can't I locate symbols for a particular subversion of a listed distribution ?*

Due to missing dependencies, some kernels specific versions may not be available here. However, you can try to edit an ISF file closely matching your needs, and check if Volatility3 can still work with it (last resort) : 

```sh
xz -d symbols.json.xz
target_banner=''
banner_path='.symbols.linux_banner.constant_data' || '.symbols.version.constant_data' # linux || mac, depending on your need
jq "$banner_path = \"$(echo -n $target_banner | base64 -w0)\"" symbols.json > symbols.patched.json
```

## macOS

Kernel debug symbols for macOS are fetched from : https://developer.apple.com/download/all. However, as Apple does not provide every build they make, some versions aren't available in this repository.
