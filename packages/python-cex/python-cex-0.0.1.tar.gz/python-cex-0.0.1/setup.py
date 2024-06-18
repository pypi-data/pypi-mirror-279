from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.1'
DESCRIPTION = 'The Cleaning and EXploration kit for Data Scientist.'
LONG_DESCRIPTION = 'A package that allows data scientist to do data exploration and cleaning in more convenient way.'

# Setting up
setup(
    name="python-cex",
    version=VERSION,
    author="John Willliam (Yande)",
    author_email="<satwikayasayande@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['pandas', 'numpy', 'matplotlib', 'scikit-learn', 'seaborn', 'scipy'],
    keywords=['python', 'data science', 'cleaning', 'exploring', 'clean', 'explore'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: Microsoft :: Windows",
    ]
)