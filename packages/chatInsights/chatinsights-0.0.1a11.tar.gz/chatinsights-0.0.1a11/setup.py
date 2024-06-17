from setuptools import find_packages, setup

with open("README.rst", "r", encoding="utf-8") as f:
    long_description = f.read()

__version__ = "0.0.1a11"
REPO_NAME = "chatInsights"
AUTHOR = "ronilpatil"
AUTHOR_EMAIL = "ronylpatil@gmail.com"
AUTHOR_USER_NAME = "ronylpatil"


setup(
    name=REPO_NAME,
    version=__version__,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    description=("whatsapp group chat analysis python package"),
    keywords=["chat analysis", "statistical analysis", "eda"],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=f"https://github.com/{AUTHOR_USER_NAME}/{REPO_NAME}",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Operating System :: MacOS",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
        "Environment :: Console",
        "Natural Language :: English",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Communications :: Chat",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Scientific/Engineering :: Visualization",
    ],
    python_requires=">=3.9",
    project_urls={
        "Source": f"https://github.com/{AUTHOR_USER_NAME}/{REPO_NAME}",
        "Bug Tracker": f"https://github.com/{AUTHOR_USER_NAME}/{REPO_NAME}/issues",
        "Changelog": f"https://github.com/{AUTHOR_USER_NAME}/{REPO_NAME}/releases",
    },
    package_dir={"": "src"},
    packages=find_packages(where="src"),
)

# ref. for classifiers: https://pypi.org/classifiers/
