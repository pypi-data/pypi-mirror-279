from setuptools import setup
from setuptools import find_packages

setup(
    name='restmapi',
    version=open('restmapi/version.txt').read(),
    packages=find_packages(),
    description='MORPHEE REST API SDK',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Xavier Dourille',
    author_email='dourille@fev.com',
    url='https://dev.azure.com/STS-Software/MORPHEE/_git/TOOLS-REST-MAPI?path=/Python',
    install_requires=[
        'requests>=2.25',
        'psutil>=5.9.8',
        'signalr-client>=0.0.7'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
    package_data={"": ["version.txt"]},    
)