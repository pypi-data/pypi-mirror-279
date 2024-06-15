from setuptools import setup, find_packages
import platform

with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name='segfault_package',
    version='0.0.3',
    author='pael',
    description='If you ever missed segfaults in Python, there you go',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/fdmx2301/segfault.git",
    packages=find_packages(),
    package_data={
        'segfault': ['../libsegfault.so', '../libsegfault.dll']
    },
    include_package_data=True,
    python_requires='>=3.6',
)
