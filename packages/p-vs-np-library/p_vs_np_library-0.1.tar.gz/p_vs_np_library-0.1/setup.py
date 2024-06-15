# setup.py
from setuptools import setup, find_packages

setup(
    name='p_vs_np_library',
    version='0.1',
    packages=find_packages(), # Add any dependencies here
    install_requires=[],
    author='Drew Simpson',
    author_email='dsimps3@icloud.com',
    description='A library for solving P vs NP problems.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/p_vs_np_library',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)

