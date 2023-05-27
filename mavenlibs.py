import sys
import json
from urllib.request import urlopen
import hashlib
from string import Template
from collections import namedtuple
from os import listdir

path = './tomcat/lib/'
files = listdir(path)


def hashfile(filepath):
    f = open(filepath, 'rb')
    readFile = f.read()
    sha1Hash = hashlib.sha1(readFile)
    sha1Hashed = sha1Hash.hexdigest()
    return sha1Hashed

def request( hash ):
    url = 'https://search.maven.org/solrsearch/select?q=1:' + \
        hash+'&wt=json&rows=1'
    response = urlopen(url).read()
    return json.loads(response.decode('utf-8'));

dep = '''
<dependency>
    <groupId> $g </groupId>
    <artifactId> $a </artifactId>
    <version> $v </version>
</dependency>
'''

deps= '''
<dependencies>
    $d
</dependencies>
'''

deb_tpl = Template(dep)
debs_tpl = Template(deps)
Jar = namedtuple('Jar',[ 'g', 'a', 'v'])

dependencies = [None]*len(files)
for i, filename in enumerate(files):
    sha1=hashfile( "%s/%s" %(path, filename))
    print("File : %i : sha1 : %s" % (i, sha1))
    obj = request( str(sha1 ))
    if obj['response']['numFound'] == 1:
        jar = Jar(obj['response']['docs'][0]['g'],
                 obj['response']['docs'][0]['a'],
                 obj['response']['docs'][0]['v'])
        dependencies[i] = jar

#         print(obj['response']['docs'][0]['a'])
#         print(obj['response']['docs'][0]['g'])
#         print(obj['response']['docs'][0]['v'])

    else :
        print('Cannot find %s' % filename)
        print(obj)
        dependencies[i] = None
deps_all = '\r\n'.join([ deb_tpl.substitute(f._asdict())for f in dependencies if f is not None ])
res = debs_tpl.substitute(d=deps_all)
print(res)

