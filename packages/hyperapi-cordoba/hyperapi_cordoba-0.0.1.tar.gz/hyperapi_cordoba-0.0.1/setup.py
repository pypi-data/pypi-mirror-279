from distutils.core import setup
setup(
    name="hyperapi_cordoba",
    packages=["hyperapi_cordoba"],
    version="0.0.1",
    description="HyperAPI's powerful apis for image and spectrum processing",
    author="HyperCorn",                   # Type in your name
    author_email="hypercorncordoba@gmail.com",      # Type in your E-Mail
    url="https://github.com/HyperCorn",
    download_url="https://github.com/HyperCorn/HyperAPI-Python-Client/releases/tag/v0.0.1",
    keywords=["IMAGES", "SPECTRUMS", "CROPS", "SATELITAL-IMAGES"],
    install_requires=[            # I get to this in a second
        "requests",
    ],
    classifiers=[
        "Development Status :: 5 - Production/Stable",

        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",

        "License :: OSI Approved :: MIT License",

        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",

    ],
)
