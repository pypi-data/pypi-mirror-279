from setuptools import setup, find_packages

setup(
    name='FamzzXMadBypass',
    version='0.1.0',
    packages=find_packages(),
    install_requires=['requests'],
    description='A module to bypass Adlink',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Famzz X Mad',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
