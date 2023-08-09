# <img src="https://cdn-icons-png.flaticon.com/128/5088/5088992.png" width="3%" height="3%"> Volatility3 symbols

![](https://img.shields.io/badge/Symbols-4258-green)

![](https://img.shields.io/badge/Ubuntu%20releases/amd64-14.04%20%7C%2016.04%20%7C%2018.04%20%7C%2020.04%20%7C%2022.04-blue)  
![](https://img.shields.io/badge/Ubuntu%20releases/i386-14.04%20%7C%2016.04%20%7C%2018.04-blue)  


## About the project 

This repository contains Volatility3 symbols in ISF (Intermediate Symbol Format) files, generated against a panel of Linux kernels. It includes most version and subversion that ever existed for a kernel release.

## Format

### Ubuntu

- Profile path : `Ubuntu/[ubuntu_version_number]/[architecture]/[kernel_flavor]/`

- Profile filename : `Ubuntu-[ubuntu_version_number]_[kernel_version]-[kernel_flavor]_[architecture].json.xz`

- Example : `Ubuntu/14.04/amd64/generic/Ubuntu-14.04_3.13.0-29.53-generic_amd64.json.xz`

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

- [ ] Debian/[amd64,i386] symbols