from setuptools import setup, find_packages

setup(
    name='xdc',
    version='1.0.4',
    description='xdc.py is a Python library for interacting with XDC (XinFin Digital Contract) tokens using web3.py',
    long_description=open('README.md', 'r', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Ziusz/xdc.py',
    author='Ziusz',
    author_email='ziusz@outlook.com',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        "Intended Audience :: Developers",
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",        
    ],
    keywords='xdc sdk web3.py smartcontract token xrc20 xrc721 xinfin digital contract web3',
    python_requires=">=3.8, <4",
    py_modules=["xdc"],
    packages=find_packages(exclude=["tests", "tests.*"]),
    install_requires=[
        'web3>=6.18.0', 
    ],
)
