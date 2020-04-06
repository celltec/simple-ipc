import os
from io import open
from setuptools import setup, find_packages

readme = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'readme.md')

if os.path.exists(readme):
    with open(readme, 'r') as fd:
        long_description = fd.read()
else:
    long_description = 'See readme.md'

setup(
    name='simple-ipc',
    version='1.2.1',
    description='Inter-process communication based on stdio',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/celltec/simple-ipc',
    project_urls={'Source': 'https://github.com/celltec/simple-ipc/tree/master/src/ipc/worker.py'},
    author='Jeremy Peters',
    author_email='contact@celltec.dev',
    keywords='ipc stdio stdin stdout send process program communicate interact transmit transfer communication interaction transmission simple',
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    python_requires='>=2.7, <4',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
    ],
)
