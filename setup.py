import os
from setuptools import setup


def read(fname):
    filename = os.path.join(os.path.dirname(__file__), fname)
    return open(filename).read().replace('#', '')

setup(
    name="livedumper",
    version="0.2.1",
    author="Thiago Kenji Okada",
    author_email="thiago.mast3r@gmail.com",
    description=("Livestreamer stream dumper"),
    license="Simplified BSD",
    keywords="video streaming downloader dumper",
    url='https://github.com/m45t3r/livedumper',
    packages=["livedumper"],
    package_dir={"": "src"},
    scripts=['src/livedumper_cli'],
    install_requires=("appdirs", "livestreamer", 'requests'),
    long_description=read('README.rst'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "Environment :: Console",
        "Operating System :: POSIX",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Multimedia :: Sound/Audio",
        "Topic :: Multimedia :: Video",
        "Topic :: Utilities",
    ],
)
