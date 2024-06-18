from setuptools import setup, find_packages


def readme():
  with open('README.md', 'r') as f:
    return f.read()


setup(
  name='cipher_easy',
  version='0.0.1',
  author='denis',
  author_email='rideofthedrums@gmail.com',
  description='This is the simplest module for quick work with cipher.',
  long_description=readme(),
  long_description_content_type='text/markdown',
  url='https://github.com/sghg228/cipher_easy',
  packages=find_packages(),
  install_requires=['requests>=2.25.1'],
  classifiers=[
    'Programming Language :: Python :: 3.11',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent'
  ],
  keywords='files speedfiles ',
  project_urls={
    'GitHub': 'https://github.com/sghg228/cipher_easy'
  },
  python_requires='>=3.6'
)