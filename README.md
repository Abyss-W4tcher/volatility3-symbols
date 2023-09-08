# <img src="https://cdn-icons-png.flaticon.com/128/5088/5088992.png" width="3%" height="3%"> Volatility3 symbols

![](https://img.shields.io/badge/Symbols-5494-seagreen?style=flat-square)

![](https://img.shields.io/badge/Ubuntu%20kernels/amd64-3.13.0%20--%3E%206.5.0-dodgerblue?labelColor=lightsteelblue&style=for-the-badge&logo=ubuntu)  
![](https://img.shields.io/badge/Ubuntu%20kernels/i386-3.13.0%20--%3E%205.4.0-darkcyan?labelColor=lightsteelblue&style=for-the-badge&logo=ubuntu)  
![](https://img.shields.io/badge/Debian%20kernels/amd64-2.6.32%20--%3E%206.4.0-dodgerblue?labelColor=lightsteelblue&style=for-the-badge&logo=debian)  
![](https://img.shields.io/badge/KaliLinux%20kernels/amd64-3.18.0%20--%3E%206.4.0-darkcyan?labelColor=lightsteelblue&style=for-the-badge&logo=kalilinux)  
![](https://img.shields.io/badge/AlmaLinux%20kernels/amd64-4.18.0%20%7C%205.14.0-dodgerblue?labelColor=lightsteelblue&style=for-the-badge&logo=almalinux)  
![](https://img.shields.io/badge/RockyLinux%20kernels/amd64-4.18.0%20%7C%205.14.0-darkcyan?labelColor=lightsteelblue&style=for-the-badge&logo=rockylinux)  

## About the project 

This repository contains Volatility3 symbols in ISF (Intermediate Symbol Format) files, generated against a panel of Linux kernels. It includes most version and subversion that ever existed for a kernel release.

## Related work 

A similar project for Volatility2 profiles is available here : https://github.com/Abyss-W4tcher/volatility2-profiles

Generate your own Volatility3 symbols with : https://github.com/Abyss-W4tcher/volatility-scripts/tree/master/symbols_builder

## Format

| Distribution | Path | Profile | Example |
| ------------ | ---- | ------- | ------- |
| Ubuntu       | Ubuntu/<*architecture*>/<*base-kernel-version*>/<*ABI*>/<*kernel-flavour*>/ | Ubuntu_<*kernel-version*>\_<*package-revision*>\_<*architecture*>.json.xz | Ubuntu/amd64/4.4.0/22/generic/Ubuntu_4.4.0-22-generic_4.4.0-22.40~14.04.1_amd64.json.xz |
| Debian       | Debian/<*architecture*>/<*base-kernel-version*>/<*ABI*>/<*kernel-flavour*>/ | Debian_<*kernel-version*>\_<*package-revision*>\_<*architecture*>.json.xz | Debian/amd64/3.1.0/1/Debian_3.1.0-1-amd64_3.1.1-1_amd64.json.xz |
| KaliLinux       | KaliLinux/<*architecture*>/<*base-kernel-version*>/<*kernel-flavour*>/ | KaliLinux_<*kernel-version*>\_<*package-revision*>\_<*architecture*>.json.xz | KaliLinux/amd64/5.2.0/KaliLinux_5.2.0-kali2-amd64_5.2.9-2kali1_amd64.json.xz |
| AlmaLinux       | AlmaLinux/<*architecture*>/<*base-kernel-version*>/ | AlmaLinux_<*kernel-version*>.<*architecture*>.json.xz | AlmaLinux/x86_64/4.18.0/AlmaLinux_4.18.0-477.13.1.el8_8.x86_64.json.xz |
| RockyLinux       | RockyLinux/<*architecture*>/<*base-kernel-version*>/ | RockyLinux_<*kernel-version*>.<*architecture*>.json.xz | RockyLinux/x86_64/4.18.0/RockyLinux_4.18.0-477.10.1.el8_8.x86_64.json.xz |

## Usage

Place every compressed symbol file you plan to use inside your `[volatility3_installation]/volatility3/symbols/linux/` directory (create it if needed).

If you cannot find the exact match for your memory dump kernel version in this repository, search the closest one available and give it a try.

## FAQ

- *Why can't I locate symbols for a particular subversion of a listed distribution ?*

Due to missing dependencies, some kernels specific versions may not be available here.  