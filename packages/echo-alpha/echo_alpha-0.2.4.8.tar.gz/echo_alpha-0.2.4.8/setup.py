from setuptools import setup, find_packages

# Replace with your library name and version
LIBRARY_NAME = 'echo_alpha'
VERSION = '0.2.4.8'

setup(
  name=LIBRARY_NAME,
  version=VERSION,
  package_dir = {"": "src"},
  packages=find_packages(where='src',
                         exclude=['tests*']),  # Exclude test directories
  author='Niro',
  author_email='niro@echo.com',
  description='ECHO AI client distributed as a python package',
  install_requires=['requests','python-dotenv'],
)
