from setuptools import setup, find_packages

VERSION = '0.0.1'
# LICENSE = 'CC BY-NC 4.0'
URL = 'https://github.com/tarek-eissa/codi'
DESCRIPTION = 'Contextual Out-of-Distribution Integration'
LONG_DESCRIPTION = 'For information on this package and its usage, please refer to the GitHub project %s' % URL

setup(
    name='pycodi',
    author="Tarek Eissa",
    version=VERSION,
    url=URL,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    # license_files=('LICENSE.txt',),
    # license=LICENSE,
    packages=find_packages(),
    install_requires=[]
)