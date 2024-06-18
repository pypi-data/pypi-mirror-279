from setuptools import setup , find_packages
classifiers = [ "Programming Language :: Python :: 3", 
                "License :: OSI Approved :: MIT License", 
                "Operating System :: OS Independent",
                "Intended Audience :: Education",
                "Development Status :: 5 - Production/Stable"]




setup(
name="abu_project",
version="0.0.1",
description="This package comes with lots of functionality which makes your work easy ! ",
long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
url = '',
author="abuawaish",
author_email="abuawaish7@gmail.com",
license='MIT',
keywords='funny',
classifiers=classifiers,
packages=find_packages(),
install_requires = ['']
)
