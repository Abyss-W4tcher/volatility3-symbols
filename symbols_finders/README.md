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