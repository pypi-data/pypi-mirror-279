import pathlib
from setuptools import find_packages, setup

with open("./requirements.txt") as req_f:
    installs = req_f.read().splitlines()
    installs = [e.split("==")[0] for e in installs]

    for e in ["build", "pip-chill", "twine"]:
        if e in installs:
            installs.remove(e)

setup(
    name="reverie_sdk",
    version="0.0.3",
    description="Reverie Language Technologies SDK",
    long_description=pathlib.Path("readme.md").read_text(),
    long_description_content_type="text/markdown",
    author="Rohnak Agarwal",
    author_email="rohnak.agarwal@reverieinc.com",
    packages=find_packages(),
    install_requires=installs,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.10",
        "Topic :: Multimedia :: Sound/Audio :: Speech",
    ],
    python_requires=">=3.8,<3.12",
    include_package_data=True,
    # entry_points={
    #     "console_scripts": ["reverie-sdk = reverie_sdk.cli:main"],
    # },
)
