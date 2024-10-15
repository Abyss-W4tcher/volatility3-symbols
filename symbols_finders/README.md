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
dwarf2json linux --elf linux-image-unsigned-5.15.0-43-generic-dbgsym_5.15.0-43.46_amd64/usr/lib/debug/boot/vmlinux-5.15.0-43-generic | xz > linux-image-unsigned-5.15.0-43-generic-dbgsym_5.15.0-43.46_amd64.json.xz
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

If you notice that the vmlinux file is stripped, it means that it does not embed debug symbols, hence making it unusable for dwarf2json use. However, you can follow the next section for a solution to generate a valid ISF.

### Kernel compilation

*Requirements* : 10GB storage, `docker`, a copy of `dwarf2json`

Inside the previously created `extracted_apk/boot/` directory, we can find the `System.map-virt` file, which contains exported kernel symbols addresses. This is half of the information needed to construct the ISF. Now, we still need to generate the kernel types, which embeds the structures definitions. 

To do so, we will compile the target Alpine Linux kernel, before merging it with the `System.map`. Place yourself in the same directory where you downloaded the `.apk` packages, then follow (and adapt when needed) the procedure :

```sh
# When available, use a close version match (here 3.14)
docker run -it -v $(pwd):/bind alpine:3.14
## Now, we are inside the container ##
# Update and install required packages
apk update
apk add nano vim sudo wget alpine-sdk

# Create a "builder" user, with sudo capabilities for convenience
adduser -D builder
addgroup builder abuild
echo "builder ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/builder
# Switch to the builder user
su - builder

# Clone the alpine aports source repository
git clone https://github.com/alpinelinux/aports
# Navigate to the main "linux-lts" source
cd aports/main/linux-lts
# Search for a commit mentioning the kernel version we want to compile
$ git --no-pager log --all --decorate=short --pretty=oneline -S '5.10.180' -- APKBUILD
fc280c1ca71ab3f3883dd3e9fb9713996f69a22d (HEAD) main/linux-lts: upgrade to 5.10.180
# Checkout to the appropriate commit
git checkout fc280c1ca71ab3f3883dd3e9fb9713996f69a22d
```

Remove the "lts" or "virt" line from APKFILE, accordingly to the kernel version you want to compile. Otherwise, both "lts" and "virt" kernel version will be compiled :

```
lts.aarch64.config
lts.armv7.config
lts.x86.config
lts.x86_64.config <-- in our case, remove this line
lts.ppc64le.config
lts.s390x.config
lts.loongarch64.config

virt.aarch64.config
virt.armv7.config
virt.ppc64le.config
virt.x86.config
virt.x86_64.config
```

```sh
# Make use of all the available CPU cores when compiling
sed -i 's/make /make -j $(nproc) /g' APKBUILD

# Regenerate checksums, fetch dependencies and kernel source
abuild checksum
abuild deps 
abuild unpack

# Set the appropriate config options
# <!> Modify the paths accordingly <!>
CONFIG_FILE="$(readlink -f config-virt.x86_64)"
CONFIG_SCRIPT="$(readlink -f src/linux-5.10/scripts/config)"
$CONFIG_SCRIPT --file "$CONFIG_FILE" --enable CONFIG_DEBUG_INFO
$CONFIG_SCRIPT --file "$CONFIG_FILE" --disable CONFIG_DEBUG_INFO_REDUCED 
$CONFIG_SCRIPT --file "$CONFIG_FILE" --disable DEBUG_INFO_COMPRESSED
$CONFIG_SCRIPT --file "$CONFIG_FILE" --disable DEBUG_INFO_SPLIT
$CONFIG_SCRIPT --file "$CONFIG_FILE" --disable DEBUG_INFO_DWARF4
$CONFIG_SCRIPT --file "$CONFIG_FILE" --disable DEBUG_INFO_BTF

# Regenerate checksums, prepare and make the kernel build (it may take a while)
abuild checksum
abuild prepare
abuild build

# Once finished, check out the build directory
ls src/build-virt.x86_64/
# Copy the vmlinux file to the host
sudo cp /src/build-virt.x86_64/vmlinux /bind/

## Back to the host ##
# Generate an ISF combining the freshly compiled vmlinux and the System.map
./dwarf2json linux --elf vmlinux --system-map extracted_apk/boot/System.map-virt > elf_sysmap.json

# Now, we need to update the banner inside the ISF, accordingly to the one from the memory sample we want to analyze
$ new_banner='Linux version 5.10.180-0-virt (buildozer@build-3-14-x86_64) (gcc (Alpine 10.3.1_git20210424) 10.3.1 20210424, GNU ld (GNU Binutils) 2.35.2) #1-Alpine SMP Thu, 18 May 2023 08:53:16 +0000'
$ printf "%s\n\0" "$new_banner" | base64 -w0; echo
TGludXggdmVyc2lvbiA1LjEwLjE4MC0wLXZpcnQgKGJ1aWxkb3plckBidWlsZC0zLTE0LXg4Nl82NCkgKGdjYyAoQWxwaW5lIDEwLjMuMV9naXQyMDIxMDQyNCkgMTAuMy4xIDIwMjEwNDI0LCBHTlUgbGQgKEdOVSBCaW51dGlscykgMi4zNS4yKSAjMS1BbHBpbmUgU01QIFRodSwgMTggTWF5IDIwMjMgMDg6NTM6MTYgKzAwMDAKAA==
```

Open your favorite text editor, and patch the "constant_data" field of the "linux_banner" symbol : 

```json
"linux_banner": {
    "type": {
    "count": 0,
    "kind": "array",
    "subtype": {
        "kind": "base",
        "name": "char"
    }
    },
    "address": <DO_NOT_CHANGE_ME>,
    "constant_data": "<CHANGE_ME>"
}
```

You should now have a fully functional ISF to help you conduct the memory investigation !

Ressources : 
- https://strfry.github.io/blog/building-alpine-kernel.html
- https://wiki.alpinelinux.org/wiki/Custom_Kernel
- https://che-adrian.medium.com/how-to-cross-compile-alpine-linux-apk-packages-fae8a75aee88
