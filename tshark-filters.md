# Tshark filters 

To do various things

Pull sni and count occurences

```
tshark -r ./file.pcapng -Tfields -e tls.handshake.extensions_server_name -Y 'tls.handshake.extensions_server_name != ""' | sort | uniq -c
```

Get certificate subject / san 
```
???
```
