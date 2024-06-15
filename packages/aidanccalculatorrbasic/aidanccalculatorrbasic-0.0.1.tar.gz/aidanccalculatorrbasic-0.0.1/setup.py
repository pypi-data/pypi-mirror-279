from setuptools import setup, find_packages

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.txt").read_text()
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='aidanccalculatorrbasic',
  version='0.0.1',
  description='A very basic calculator',
  long_description= long_description,
  long_description_content_type='text/markdown',
  url='',  
  author='Aidan Cronin',
  author_email='aidancronin2@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='calculator', 
  packages=find_packages(),
  install_requires=[''],
)