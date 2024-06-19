'''
Author: Devin
Date: 2024-06-19 10:06:24
LastEditors: Devin
LastEditTime: 2024-06-19 12:01:53
Description: 

Copyright (c) 2024 by Devin, All Rights Reserved. 
'''
from glob import glob

from setuptools import setup
import os

VERSION = '2.1.2'
CMAPSFILE_DIR = os.path.join('./cmaps/colormaps')


def write_version_py(version=VERSION, filename='cmaps/_version.py'):
    cnt = '# THIS FILE IS GENERATED FROM SETUP.PY\n' + \
          '__version__ = "%(version)s"\n'
    a = open(filename, 'w')
    try:
        a.write(cnt % {'version': version})
    finally:
        a.close()


def _listfname():
    l = {}

    l.update({'ncl': {
        'p': 'os.path.join(CMAPSFILE_DIR, "ncar_ncl", ',
        'l': sorted(glob(os.path.join(CMAPSFILE_DIR, 'ncar_ncl/*.rgb')))}})
    l.update({'self_defined': {
        'p': 'os.path.join(CMAPSFILE_DIR, "self_defined", ',
        'l': sorted(glob(os.path.join(CMAPSFILE_DIR, 'self_defined/*.rgb')))}})
    l.update({'cmcrameri': {
    'p': 'os.path.join(CMAPSFILE_DIR, "cmcrameri", ',
    'l': sorted(glob(os.path.join(CMAPSFILE_DIR, 'cmcrameri/*.rgb')))}})
    return l


def write_cmaps(template_file='./cmaps.template'):
    with open(template_file, 'rt') as f:
        c = f.read()
    l = _listfname()
    for t in l.keys():
        for cmap_file in l[t]['l']:
            cname = os.path.basename(cmap_file).split('.rgb')[0]
            # start with the number will result illegal attribute
            if cname[0].isdigit() or cname.startswith('_'):
                cname = 'N' + cname
            if '-' in cname:
                cname =  'cmaps_' + cname.replace('-', '_')
            if '+' in cname:
                cname =  'cmaps_' + cname.replace('+', '_')
            c += '    @property\n'
            c += '    def {}(self):\n'.format(cname)
            c += '        cname = "{}"\n'.format(cname)
            c += '        try:\n'
            c += '            return get_cmap(cname)\n'
            c += '        except:\n'
            c += '            cmap_file = {} "{}")\n'.format(l[t]['p'], os.path.basename(cmap_file))
            c += '            cmap = Colormap(self._coltbl(cmap_file), name=cname)\n'
            c += '            register_cmap(name=cname, cmap=cmap)\n'
            c += '            return cmap\n\n'

            c += '    @property\n'
            c += '    def {}(self):\n'.format(cname + '_r')
            c += '        cname = "{}"\n'.format(cname + '_r')
            c += '        try:\n'
            c += '            return get_cmap(cname)\n'
            c += '        except:\n'
            c += '            cmap_file = {} "{}")\n'.format(l[t]['p'], os.path.basename(cmap_file))
            c += '            cmap = Colormap(self._coltbl(cmap_file)[::-1], name=cname)\n'
            c += '            register_cmap(name=cname, cmap=cmap)\n'
            c += '            return cmap\n\n'

    cmapspy = './cmaps/cmaps.py'
    with open(cmapspy, 'wt') as fw:
        fw.write(c)


write_version_py()
write_cmaps()
setup(
    name='cmaps-devin',
    author='Devin Long',
    version=VERSION,
    author_email='long.sc@qq.com',
    packages=['cmaps', ],
    package_data={'cmaps': ['colormaps/ncar_ncl/*',
                            'colormaps/self_defined/*',
                            'colormaps/cmcrameri/*'
                            ], },
    data_files=[('', ['cmaps.template', 'LICENSE']),],
    url='',
    license='LICENSE',
    description='',
    long_description='',
    install_requires=['matplotlib', 'numpy', 'packaging'],
)
