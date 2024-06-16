try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
    
from mtdl.metadata import __version__, __author__, __author_email__

with open("LICENSE-en", "r") as file:
    license = file.read()
    
with open("README.md", "r") as f2:
    desp = f2.read()

setup_data = dict(name="mtdl", 
    version=__version__, 
    author_email=__author_email__, 
    author=__author__, 
    license=license, 
    description="Python multi-thread file downloader.", 
    long_description=desp, 
    long_description_content_type= "text/markdown",
    install_requires=["colorama", "tqdm"], 
    entry_points={"console_scripts":["mtdl = mtdl.cli:main"]}, 
    classifiers=[
        "Programming Language :: Python", 
        "Programming Language :: Python :: 3 :: Only", 
        "Topic :: Internet", 
        "Topic :: Internet :: WWW/HTTP", 
        ])

if __name__ == "__main__":
    setup(**setup_data)