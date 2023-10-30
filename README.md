# <img src="https://cdn-icons-png.flaticon.com/128/5088/5088992.png" width="3%" height="3%"> Volatility3 symbols

![](https://img.shields.io/badge/Symbols-6588-seagreen?style=flat-square)

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

Use the "banners/banners_plain.json" file to match banners and symbols quickly.

## FAQ

- *Why can't I locate symbols for a particular subversion of a listed distribution ?*

Due to missing dependencies, some kernels specific versions may not be available here. However, you can try to edit an ISF file closely matching your needs, and check if Volatility3 can still work with it (last resort) : 

```sh
# Edit :
symbols_filename=''
new_banner=''
banner_path='.symbols.linux_banner.constant_data' OR '.symbols.version.constant_data' # linux || mac, depending on your need
# Do not edit :
patched_filename=$(basename "$symbols_filename" .json.xz).patched.json
xz -d "$symbols_filename"
jq "$banner_path = \"$(printf "%s\0" $new_banner | base64 -w0)\"" $(basename "$symbols_filename" .xz) > $patched_filename
cat $patched_filename | jq -r "$banner_path" | base64 -d | xxd
```

Be aware that changing the banner won't make everything work by magic, as some other things like KASLR shift still need to match.

## macOS

Kernel debug symbols for macOS are fetched from : https://developer.apple.com/download/all. However, as Apple does not provide every build they make, some versions aren't available in this repository.
Here are some discussions about it :

- https://github.com/volatilityfoundation/volatility3/issues/155
- https://github.com/volatilityfoundation/volatility3/issues/541
