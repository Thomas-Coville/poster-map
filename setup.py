import os, re
from setuptools import setup, find_packages

req_file = os.path.join(os.path.abspath(os.path.dirname(__file__)),'requirements.txt' )

with open(req_file) as f:
    install_requires = f.read().strip().split('\n')

setup(
    name='posters',
    version='0.1.0',
    url='https://github.com/Thomas-Coville/poster-map.git',
    author='Thomas COVILLE',        
    description='toy API to generate High definition images from Google Maps',
    packages=find_packages(),    
    zip_safe=False,
    install_requires=install_requires,
)