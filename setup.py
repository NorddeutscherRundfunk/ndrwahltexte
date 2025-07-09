from setuptools import setup
from setuptools import find_packages

with open('requirements.txt') as f:
    content = f.readlines()
requirements = [x.strip() for x in content if 'git+' not in x]

setup(name='ndrwahltexte',
      version='0.1',
      description='Erstellt Fließtext basierend auf dem Wahlergebnis',
      url='http://github.com/',
      author='Lalon Sander',
      author_email='l.sander.fm@ndr.de',
      license='MIT',
      packages=find_packages(),
      install_requires=requirements,
      zip_safe=False)