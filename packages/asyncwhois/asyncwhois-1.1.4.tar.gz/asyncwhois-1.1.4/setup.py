import setuptools
import pathlib

base_dir = pathlib.Path(__file__).parent.resolve()


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


def get_version(location: str) -> str:
    with open((base_dir / location).absolute().resolve()) as file:
        for line in file.readlines():
            if line.startswith("__version__"):
                return line.split(" = ")[-1].strip().replace('"', "")
        else:
            raise RuntimeError("Unable to find version string.")


setuptools.setup(
    name="asyncwhois",
    version=get_version("asyncwhois/__init__.py"),
    author="Joseph Obarzanek",
    author_email="pogzyb@umich.edu",
    description="Python utility for querying and parsing WHOIS information for Domains, IPv4s, IPv6s, and AS numbers.",
    long_description=long_description,
    license="MIT",
    install_requires=[
        "python-socks[asyncio]>=2.0.2",
        "tldextract>=3.2.0",
        "whodap>=0.1.10",
    ],
    classifiers=[
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Software Development",
        "Topic :: Security",
        "Framework :: AsyncIO",
    ],
    url="https://github.com/pogzyb/asyncwhois",
    packages=setuptools.find_packages(),
    package_dir={"asyncwhois": "asyncwhois"},
    python_requires=">=3.9",
)
