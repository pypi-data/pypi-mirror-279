from setuptools import setup, find_packages

VERSION = "0.0.1"
DESCRIPTION = "Basic finance calculator tool"

setup(
    name="pynance-calc",
    version=VERSION,
    author="Jake Williamson",
    author_email="<brianjw88@gmail.com>",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=[
        "requests"
    ],
    keywords=["python",],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
    ],
)