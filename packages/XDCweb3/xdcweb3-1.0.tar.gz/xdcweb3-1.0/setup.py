from setuptools import setup, find_packages

setup(
    name='XDCweb3',
    version='1.0',
    description='XDC SDK that works with the new web3.py',
    long_description=open('README.md', 'r', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Ziusz/XDCweb3.py',
    author='Ziusz',
    author_email='ziusz@outlook.com',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    keywords='xdc sdk web3.py smartcontract token xrc20 xrc721 xinfin digital contract web3',
    packages=find_packages("XDCweb3"),
    install_requires=[
        'web3', 
    ],
)
