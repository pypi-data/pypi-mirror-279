from distutils.core import setup
setup(
    name="hypercorn_api",
    packages=["hypercorn_api"],
    version="0.0.2",
    description="HyperCornAPI powerful api for image and spectrum processing.",
    long_description="HyperCornAPI, developed by Hypercorn, is a foundational API designed to seamlessly integrate with HyperApp, an advanced application tailored for crop classification. This documentation provides comprehensive guidance on endpoints, methods, and best practices for developers seeking to harness HyperAPI's powerful capabilities in image and spectrum processing.",
    author="HyperCorn",                   # Type in your name
    author_email="hypercorncordoba@gmail.com",      # Type in your E-Mail
    url="https://github.com/HyperCorn/HyperCornAPI-Python-Client",
    download_url="https://github.com/HyperCorn/HyperCornAPI-Python-Client/releases/tag/0.0.2",
    keywords=["IMAGES", "SPECTRUMS", "CROPS"],
    install_requires=[            # I get to this in a second
        "requests",
    ],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
)
