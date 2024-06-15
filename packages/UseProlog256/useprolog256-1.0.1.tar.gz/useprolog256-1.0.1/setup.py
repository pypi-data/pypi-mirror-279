from setuptools import setup, find_packages

def readme():
  with open('README.md', 'r') as f:
    return f.read()

setup(
  name='UseProlog256',
  version='1.0.1',
  author='IvanP',
  author_email='I.popovich2002@gmail.com',
  description='This is my first module',
  long_description=readme(),
  long_description_content_type='text/markdown',
  url='https://github.com/Ivan101002/TestRepOnPython',
  packages=find_packages(),
  install_requires=['requests>=2.25.1'],
  classifiers=[
    'Programming Language :: Python :: 3.11',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent'
  ],
  keywords='example python prolog',
  python_requires='>=3.7'
)