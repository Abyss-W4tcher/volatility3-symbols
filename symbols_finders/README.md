## Ubuntu symbols finder

Sample run : 

```sh
$ python3 ubuntu_symbols_finder.py 
Usage : python3 ubuntu_symbols_finder.py '[linux_banner]'. Example :
python3 ubuntu_symbol_finder.py 'Linux version 5.15.0-43-generic (buildd@lcy02-amd64-076) (gcc (Ubuntu 11.2.0-19ubuntu1) 11.2.0, GNU ld (GNU Binutils for Ubuntu) 2.38) #46-Ubuntu SMP Tue Jul 12 10:30:17 UTC 2022 (Ubuntu 5.15.0-43.46-generic 5.15.39)'

$ python3 ubuntu_symbols_finder.py 'Linux version 5.15.0-43-generic (buildd@lcy02-amd64-076) (gcc (Ubuntu 11.2.0-19ubuntu1) 11.2.0, GNU ld (GNU Binutils for Ubuntu) 2.38) #46-Ubuntu SMP Tue Jul 12 10:30:17 UTC 2022 (Ubuntu 5.15.0-43.46-generic 5.15.39)'
Debug symbols should be available at http://launchpadlibrarian.net/612559099/linux-image-unsigned-5.15.0-43-generic-dbgsym_5.15.0-43.46_amd64.ddeb. Here is a typical procedure to create the ISF :

wget http://launchpadlibrarian.net/612559099/linux-image-unsigned-5.15.0-43-generic-dbgsym_5.15.0-43.46_amd64.ddeb
dpkg-deb -x linux-image-unsigned-5.15.0-43-generic-dbgsym_5.15.0-43.46_amd64.ddeb linux-image-unsigned-5.15.0-43-generic-dbgsym_5.15.0-43.46_amd64/
dwarf2json linux --elf linux-image-unsigned-5.15.0-43-generic-dbgsym_5.15.0-43.46_amd64/usr/lib/debug/boot/5.15.0-43-generic | xz > linux-image-unsigned-5.15.0-43-generic-dbgsym_5.15.0-43.46_amd64.json.xz
```

## Alpine symbols finder 

Let's use the sample banner : 

> Linux version 5.10.180-0-virt (buildozer@build-3-14-x86_64) (gcc (Alpine 10.3.1_git20210424) 10.3.1 20210424, GNU ld (GNU Binutils) 2.35.2) #1-Alpine SMP Thu, 18 May 2023 08:53:16 +0000

- Navigate to the Alpine package mirror : https://dl-cdn.alpinelinux.org/alpine/
- Click on the appropriate release version (buildozer@build-**3-14**-x86_64) : https://dl-cdn.alpinelinux.org/alpine/v3.14/
- Choose the "main" repository : https://dl-cdn.alpinelinux.org/alpine/v3.14/main/
- Click on the appropriate architecture (buildozer@build-3-14-**x86_64**) : https://dl-cdn.alpinelinux.org/alpine/v3.14/main/x86_64/
- Search for packages starting with `linux-virt` (5.10.180-0-**virt**) :

```
linux-virt-5.10.180-r0.apk                         18-May-2023 11:41     24M
linux-virt-dev-5.10.180-r0.apk                     18-May-2023 11:41     18M
```

- Right click on `linux-virt-5.10.180-r0.apk` (not the `-dev` one) and copy the link
- Execute the following command to get the appropriate `vmlinux` binary :

```sh
# Download the package
wget https://dl-cdn.alpinelinux.org/alpine/v3.14/main/x86_64/linux-virt-5.10.180-r0.apk
# Extract it
mkdir extracted_apk/
tar -xzf linux-virt-5.10.180-r0.apk -C extracted_apk
# Download the vmlinux extraction tool for linux kernel
wget https://raw.githubusercontent.com/torvalds/linux/master/scripts/extract-vmlinux -O extract-vmlinux
# Extract the vmlinux file
chmod +x ./extract-vmlinux
./extract-vmlinux extracted_apk/boot/vmlinuz-virt > vmlinux-virt
# Verify the file type and banner
file vmlinux-virt
vmlinux-virt: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), statically linked, BuildID[sha1]=fded3bc49de40d90abb2f8702f25796b92ca5385, stripped
grep -a 'Linux version' vmlinux-virt
Linux version 5.10.180-0-virt (buildozer@build-3-14-x86_64) (gcc (Alpine 10.3.1_git20210424) 10.3.1 20210424, GNU ld (GNU Binutils) 2.35.2) #1-Alpine SMP Thu, 18 May 2023 08:53:16 +0000
```

Then, you can construct the ISF with dwarf2json.
