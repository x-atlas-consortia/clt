from setuptools import setup

from clt.config import get_config, generate_pypi_readme

config = get_config()
NAME = config["PKG_NAME"]
AUTHOR = config["PKG_AUTHOR"]
AUTHOR_EMAIL = config["PKG_AUTHOR_EMAIL"]

setup(
    name=NAME,
    description="A command line interface to download multiple files and directories from Globus file transfer "
                "service using a manifest file.",
    version=config["PKG_VERSION"],
    packages=["clt"],
    python_requires=">=3.6",
    entry_points=f"""
        [console_scripts]
        {NAME}=clt.__main__:main
    """,
    author=AUTHOR,
    author_email=config["PKG_AUTHOR_EMAIL"],
    long_description=generate_pypi_readme(config),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    include_package_data=True,
    install_requires=[
        "certifi>=2021.10.8",
        "charset-normalizer>=2.0.10",
        "idna>=3.3",
        "requests>=2.27.1",
        "urllib3>=1.26.8",
        "globus-cli>=3.1.4",
    ],
    keywords=[
        f"{AUTHOR} CLT",
        "python"
    ]
)
