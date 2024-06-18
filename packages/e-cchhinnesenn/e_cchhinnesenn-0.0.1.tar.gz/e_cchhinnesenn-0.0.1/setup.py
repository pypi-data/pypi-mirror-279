import setuptools
import os
import requests


def md_to_rst(from_file, to_file):
    r = from_file
    with open(to_file, 'wb') as f:
        True
#        f.write("fuck python")


md_to_rst("README.md", "README.rst")


if os.path.exists('README.rst'):
    long_description = open('README.rst', encoding='utf-8').read()
    long_description = 'Add a fallback short description here'
else:
    long_description = 'Add a fallback short description here'

if os.path.exists('requirements.rst'):
    install_requires = open('requirements.rst').read().split('\n')
else:
    install_requires = []

setuptools.setup(
    name='e_cchhinnesenn',
    version='0.0.1',
    auther='lizhixue',
    license='MIT License',
    auther_email='blizzard_xue@sina.com',
    description='Get start of twine',
    long_description=long_description,
    long_description_content_type='text/x-rst',
    url="https://github.com/blizzard_xue/e_cchhinnesenn",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
    install_requires=install_requires,
    package_data={
        'e_cchhinnesenn': ['source/*.txt', "source/*.json"],
    },
    entry_point={

        'console_scripts': [
            'e_cchhinnesenn=e_cchhinnesenn.run:main'
        ]
    }
)    


