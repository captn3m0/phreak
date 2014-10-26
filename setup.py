import sys

from setuptools import setup
from setuptools import find_packages


requirements = ['requests']
if sys.version_info < (2, 7):
    requirements.append('argparse')

setup(name='phreak',
      version='0.0.2',
      description='Product Hunt app that sits in your System Tray',
      long_description='PHreak is a simple Product Hunt linux application that lets you current PH stories in your System Tray.',
      keywords='product hunt producthunt phreak tray',
      url='http://captnemo.in/phreak',
      author='Abhay Rana',
      author_email='me@captnemo.in',
      license='MIT',
      packages=find_packages(),
      package_data={
          'phreak.data': ['phreak.png']
      },
      install_requires=[
          'requests>=2.2.1'
      ],
      entry_points={
          'console_scripts': ['phreak = phreak:main'],
      },
      zip_safe=False)
