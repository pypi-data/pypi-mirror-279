from setuptools import setup 

VERSION = '0.1.2'
DESCRIPTION = 'A Python wrapper for Invidious API'

with open("README.md", "r") as ofile:
    LONG_DESCRIPTION = ofile.read()

packages = [
    'invidious', 'invidious.enums', 'invidious.types'
]

# Setting up
setup(
    name="invidious.py",
    version=VERSION,
    author="loliconshik3",
    author_email="loliconshik3@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=packages,
    install_requires=['requests', 'dataclasses'],
    keywords=['python', 'invidious', 'youtube', 'video', 'api'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows"
    ]
)
