# Clean up a linux guest disk in vmware workstation.
Can drastically reduce the size taken up on the host by the guests VM disk files.

**from https://superuser.com/questions/211798/how-to-reduce-the-size-of-vmware-disk**

1. Defrag 

`sudo e4defrag / >/dev/null 2>&1`

2. zero fill. Reboot into gparted iso (because disk must be unmounted or mounted as ro),  then

 `zerofree /dev/sda<X>`
 
3. Compact disk from Settings -> Hard Disk -> Compact
