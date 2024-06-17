from setuptools import setup, find_packages

setup(
    name='packtxt',
    version='0.1.0',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'packtxt=packtxt.cli:main',
        ],
    },
    install_requires=[
        # List dependencies here
    ],
    author='Matt Daniele',
    author_email='contact@mattdaniele.com',
    description='A tool to pack and unpack directories to/from .txt files with Git branch support',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/digitaluniverse/packtxt',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
