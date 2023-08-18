# <img src="https://cdn-icons-png.flaticon.com/128/5088/5088992.png" width="3%" height="3%"> Volatility3 symbols

![](https://img.shields.io/badge/Symbols-6289-green)

![](https://img.shields.io/badge/Ubuntu%20releases/amd64-14.04%20%7C%2016.04%20%7C%2018.04%20%7C%2020.04%20%7C%2022.04-blue)  
![](https://img.shields.io/badge/Ubuntu%20releases/i386-14.04%20%7C%2016.04%20%7C%2018.04-blue)    
![](https://img.shields.io/badge/Debian%20major%20kernels/amd64-2.6.32%20--%3E%206.4.0-blue)  
![](https://img.shields.io/badge/AlmaLinux%20releases/amd64-8.8%20%7C%209.2-blue)  
![](https://img.shields.io/badge/RockyLinux%20releases/amd64-8.8%20%7C%209.2-blue)  
![](https://img.shields.io/badge/KaliLinux%20major%20kernels/amd64-3.18.0%20--%3E%206.4.0-blue)


## About the project 

This repository contains Volatility3 symbols in ISF (Intermediate Symbol Format) files, generated against a panel of Linux kernels. It includes most version and subversion that ever existed for a kernel release.

## Format

### Ubuntu

- Symbols path : `Ubuntu/[ubuntu_version_number]/[architecture]/[kernel_flavor]/`

- Symbols filename : `Ubuntu-[ubuntu_version_number]_[kernel_version]-[kernel_flavor]_[architecture].json.xz`

- Example : `Ubuntu/14.04/amd64/generic/Ubuntu-14.04_3.13.0-29.53-generic_amd64.json.xz`

### Debian

- Symbols path : `Debian/[architecture]/[kernel_release]/[package_revision]/[kernel_flavor_if_specified]/`

- Symbols filename : `Debian_[kernel_release]-[package_revision]-[architecture]_[debian_revision]_[architecture].json.xz`

- Example : `Debian/amd64/4.1.0/1/rt/Debian_4.1.0-1-rt-amd64_4.1.3-1_amd64.json.xz`

### AlmaLinux

- Symbols path : `AlmaLinux/[version_number]/[architecture]/[kernel].el[version_number].[architecture]/`

- Symbols filename : `AlmaLinux_[kernel].el[version_number].[architecture].json.xz`

- Example : `AlmaLinux/8.8/x86_64/4.18.0-477.10.1.el8_8.x86_64/AlmaLinux_4.18.0-477.10.1.el8_8.x86_64.json.xz`

### RockyLinux

- Symbols path : `AlmaLinux/[version_number]/[architecture]/[kernel].el[version_number].[architecture]/`

- Symbols filename : `RockyLinux_[kernel].el[version_number].[architecture].json.xz`

- Example : `RockyLinux/8.8/x86_64/4.18.0-477.10.1.el8_8.x86_64/RockyLinux_4.18.0-477.10.1.el8_8.x86_64.json.xz`

### KaliLinux

- Symbols path : `KaliLinux/[architecture]/[kernel_release_splitted_after_two_dots]/`

- Symbols filename : `KaliLinux_[kernel_release]_[kernel_version]_[architecture].zip`

- Example : `KaliLinux/amd64/4.15/KaliLinux_4.15.0-kali2-amd64_4.15.11-1kali1_amd64.json.xz`

## Usage

Place every compressed symbol file you plan to use inside your `[volatility3_installation]/volatility3/symbols/linux/` directory (create it if needed).

Be aware that including too much content inside the symbols directory will slow down Volatility3.

If you cannot find the exact match for your memory dump kernel version in this repository, search the closest one available and give it a try.

## Notes

Due to deprecated, experimental or unstable states, some kernels specific versions may not be available here.  

Symbols aren't tested against memory dumps, please open an issue if needed.

## Related work 

A similar project for Volatility2 profiles is available here : https://github.com/Abyss-W4tcher/volatility2-profiles

A project to generate your own profiles and symbols is available here : https://github.com/Abyss-W4tcher/volatility-scripts/tree/master/profiles_and_symbols_builders


## Roadmap

- [ ] Debian/i386 symbols
