from setuptools import setup, find_packages

setup(name='kdb-testing',
      version='0.0.1',
      url='https://github.com/Trucnt/kdb-core',
      license='MIT',
      author='Trucnt',
      author_email='trucnt88@gmail.com',
      description='The automation testing framework using Selenium, Python and Pytest. '
                  'This developed base on POM pattern',
      packages=find_packages(exclude=['data', 'docs', 'examples', 'unit_test']),
      # long_description=open('README.md').read(),
      zip_safe=False)
