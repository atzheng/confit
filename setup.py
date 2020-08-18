from setuptools import setup

setup(name='ficus',
      version='0.1',
      description='',
      url='https://github.com/atzheng/configurator',
      author='Andy Zheng',
      author_email='atz@mit.edu',
      license='MIT',
      packages=['ficus'],
      install_requires=['funcy', 'codenamize', 'pyyaml', 'pandas'],
      zip_safe=False)
