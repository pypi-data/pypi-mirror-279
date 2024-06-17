from setuptools import setup, find_packages

def readme():
  with open('README.md', 'r') as f:
    return f.read()

setup(
  name='advancedeconmodels',
  version='1.0.1',
  author='pom',
  author_email='',
  description='This is my first module',
  long_description=readme(),
  long_description_content_type='text/markdown',
  url='https://github.com/powerpom/advancedmodels/archive/master.zip',
  download_url='https://github.com/powerpom/advancedmodels/archive/master.zip',
  packages=find_packages(),
  install_requires=['requests>=2.25.1'],
  classifiers=[
    'Programming Language :: Python :: 3.11',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent'
  ],
  keywords='',
  project_urls={
    'Documentation': 'https://github.com/powerpom/advancedmodels'
  },
  python_requires='>=3.7'
)