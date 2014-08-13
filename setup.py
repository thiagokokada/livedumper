import os
import sys
from setuptools import setup


def read(fname):
    filename = os.path.join(os.path.dirname(__file__), fname)
    return open(filename).read().replace('#', '')

if sys.version_info < (3,2,0):
    sys.exit("Sorry, this program is compatible with Python 3.2+ only")

setup(
    name="livedumper",
    version="0.1.2",
    author="Thiago Kenji Okada",
    author_email="thiago.mast3r@gmail.com",
    description=("Livestreamer stream dumper"),
    license="Simplified BSD",
    keywords="video streaming downloader dumper",
    url='https://github.com/m45t3r/livedumper',
    packages=["livedumper"],
    package_dir={"": "src"},
    scripts=['src/livedumper_cli'],
    install_requires=("livestreamer"),
    long_description=read('README.rst'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "Environment :: Console",
        "Operating System :: POSIX",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Multimedia :: Sound/Audio",
        "Topic :: Multimedia :: Video",
        "Topic :: Utilities",
    ],
)
