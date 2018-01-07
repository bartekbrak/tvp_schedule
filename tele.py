"""
Downloads Polish National Television daily schedule txt files, cleans them up
and presents as simple HTML file to be parsed by screen reader.

Avoids dependencies.
Runs on Python 3.4+

The destination on my VPS is hardcoded. 

"""
import datetime
from urllib.request import urlretrieve

import re

DEST = '/var/www/andrzej/'

map_ = {
    'historia': 'https://www.tvp.pl/prasa/TVPHistoria/p{:%m%d}_TKH.txt',
    'info':     'https://www.tvp.pl/prasa/TVPInfo/p{:%m%d}_INF.txt',
    'kultura':  'https://www.tvp.pl/prasa/TVPKultura/p{:%m%d}_T5D.txt',
    'hd':       'https://www.tvp.pl/prasa/TVPHD/p{:%m%d}_KHSH.txt',
    'seriale':  'https://www.tvp.pl/prasa/TVPSeriale/p{:%m%d}_TRS.txt',
}
template = '<html><head><meta charset="utf-8"></head><body><pre>\n%s\n</pre></body></html>'
clean_res = {
    re.compile('Dla małoletnich od lat \d+'): '',
    re.compile('Bez ograniczeń wiekowych'): '',
    re.compile('\s*-\s*txt\.?\s*str\.?\s*\d+\s*(AD|\d+\')?'): '',
    re.compile('wyk\.\s*'): 'występują ',
    re.compile('odc\.\s*'): 'odcinek ',
    re.compile('kraj prod\.\s*'): 'kraj produkcji ',
    re.compile('reż\.\s*'): 'reżyseria ',
    re.compile('(\d+)/(\d+)'): r'\1 z \2',
    re.compile('STEREO(\s*/\s*DOLBY)?( E)?'): '',
    re.compile('\s*16:9,?'): '',

}


def clean(lines):
    out = ''
    for line in lines.split('\n'):
        for RE, repl in clean_res.items():
            line = RE.sub(repl, line)
        out += line + '\n'
    return out


def touchopen(filename, *args, **kwargs):
    # https://stackoverflow.com/a/10350773
    open(filename, "a").close() # "touch" file
    return open(filename, *args, **kwargs)

for channel, url in map_.items():
    url = url.format(datetime.datetime.now())
    out_filename = DEST + '%s.html' % channel
    urlretrieve(url, out_filename)
    print(url, out_filename)
    with touchopen(out_filename, 'r+') as f:
        current = clean(f.read())
        f.seek(0)
        f.write(template % current)
        f.truncate()
