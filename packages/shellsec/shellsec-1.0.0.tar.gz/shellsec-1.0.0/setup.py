# setup.py

from setuptools import setup, find_packages

setup(
    name='shellsec',
    version='1.0.0',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'shellsec=shellsec.core:main',
        ],
    },
    install_requires=[],
    author='Fidal',
    author_email='mrfidal@proton.me',
    description='A tool to encrypt and decrypt Bash scripts using Base64 encoding.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/ByteBreach/shellsec',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
