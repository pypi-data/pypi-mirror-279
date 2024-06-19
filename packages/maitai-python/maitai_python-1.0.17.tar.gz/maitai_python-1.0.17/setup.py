# setup.py

from setuptools import setup, find_packages
with open("maitai/version.py") as version_file:
    version = version_file.read().strip()

setup(
    name='maitai-python',
    version=version,
    packages=find_packages(exclude=("maitai_back", "maitai_back.*")),
    install_requires=[
        'requests',
        'openai',
        'betterproto',
        'httpx',
        'aiohttp',
        'betterproto==2.0.0b6',
        'websocket-client',
    ],
    # Optional metadata
    author='Maitai',
    author_email='support@trymaitai.ai',
    description='Maitai SDK for Python',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://docs.trymaitai.ai',
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
)
