from setuptools import setup

# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(name='neuro_fuzzy_matrix',
      version='1.0',
      description='neuro fuzzy matrix',
      packages=['neuro_fuzzy_matrix'],
      author_email='epishina.nata@bk.ru',
      zip_safe=False)
