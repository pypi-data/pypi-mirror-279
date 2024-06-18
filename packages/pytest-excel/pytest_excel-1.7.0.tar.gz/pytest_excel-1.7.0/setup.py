import os
import re
import io

from setuptools import setup



setup(name='pytest-excel',
      version='1.7.0',
      description='pytest plugin for generating excel reports',
      long_description=io.open('README.rst', encoding='utf-8', errors='ignore').read(),
      author='santosh',
      author_email=u'santosh.srikanta@gmail.com',
      url=u'https://github.com/ssrikanta/pytest-excel',
      license = 'MIT',
      license_file = 'LICENSE',
      packages=['pytest_excel'],
      entry_points={'pytest11': ['excel = pytest_excel.pytest_excel']},
      install_requires=['pytest>3.6', 'pandas'],
      keywords='py.test pytest excel report',
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Framework :: Pytest',
          'Intended Audience :: Developers',
          ' License :: OSI Approved :: MIT License',
          'Operating System :: POSIX',
          'Operating System :: Microsoft :: Windows',
          'Operating System :: MacOS :: MacOS X',
          'Topic :: Software Development :: Testing',
          'Topic :: Software Development :: Quality Assurance',
          'Topic :: Software Development :: Libraries',
          'Topic :: Utilities',
          'Programming Language :: Python :: 3.8',
          'Programming Language :: Python :: 3.9',
          'Programming Language :: Python :: 3.10',
          'Programming Language :: Python :: 3.11',
          'Programming Language :: Python :: 3.12',

      ]
      )

