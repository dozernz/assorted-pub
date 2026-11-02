#!/usr/bin/env python3

import sys
import json
from urllib.request import urlopen
import hashlib
from concurrent.futures import ThreadPoolExecutor, as_completed
from string import Template
from collections import namedtuple
from os import listdir
import os

path = os.getcwd()
all_files = listdir(path)

get_sources = True

files = list(filter(lambda x:x.endswith(".jar"), all_files))

num_threads = 6

def hashfile(filepath):
    f = open(filepath, 'rb')
    readFile = f.read()
    sha1Hash = hashlib.sha1(readFile)
    sha1Hashed = sha1Hash.hexdigest()
    return sha1Hashed

def request( hash ):
    url = 'https://search.maven.org/solrsearch/select?q=1:' + hash+'&wt=json&rows=1'
    response = urlopen(url).read()
    return json.loads(response.decode('utf-8'));


def do_job(sha1,filename):
    obj = request( str(sha1 ))
    if obj['response']['numFound'] == 1:
        jar = Jar(obj['response']['docs'][0]['g'],
                 obj['response']['docs'][0]['a'],
                 obj['response']['docs'][0]['v'])

    else :
        jar =None

    return jar


dep = '''   <dependency>
        <groupId>$g</groupId>
        <artifactId>$a</artifactId>
        <version>$v</version>
    </dependency>
'''

deps= '''
<dependencies>
    $d
</dependencies>
'''

if get_sources:
    deps+='''
<build>
	<plugins>
        <plugin>
            <artifactId>maven-dependency-plugin</artifactId>
            <executions>
                <execution>
                    <id>download-sources</id>
                    <goals>
                        <goal>sources</goal>
                    </goals>
                </execution>
            </executions>
        </plugin>
	</plugins>
</build>
'''

deb_tpl = Template(dep)
debs_tpl = Template(deps)
Jar = namedtuple('Jar',[ 'g', 'a', 'v'])

dependencies = [None]*len(files)
futures_dict = {}
results = []
fails =[]

with ThreadPoolExecutor(max_workers=num_threads) as executor:
    for i, filename in enumerate(files):
        sha1=hashfile( "%s/%s" %(path, filename))
        print("File : %s : sha1 : %s" % (filename, sha1))
        future = executor.submit(do_job, sha1,filename)
        futures_dict[future] = (sha1, filename)

    for future in as_completed(futures_dict):
        sha1, filename = futures_dict[future]
        try:
            result = future.result()
            if result:
                dependencies.append(result)

        except Exception as e:
            print(f"Thread generated an exception while processing {filename}: {e}")
        else:
            if result:
                print(f"Thread successfully processed {filename}, Result: {result}")
            else:
                fails.append((filename,sha1))
                print(f"{filename} {sha1} not found",file=sys.stderr)




deps_all = '\r\n'.join([ deb_tpl.substitute(f._asdict())for f in dependencies if f is not None ])
res = debs_tpl.substitute(d=deps_all)
outf = open("found.xml",'w')
outf.write(res)

failf = open("fails.log",'w')
for t in fails:
    failf.write(f"{t[0]},{t[1]}\n")

print(f"Written to found.xml")
