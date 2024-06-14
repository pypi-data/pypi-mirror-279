from setuptools import setup, find_packages

setup(
    name="quick_yaml",
    version="1.0b",
    author="Sivarajan R",
    author_email="sivarajan931@gmail.com",
    description="A simple and easy-to-use database for home automation projects",
    long_description=open('../../README.md').read(),
    long_description_content_type="text/markdown",
    url="https://gitlab.com/eazy-home-admin/BreezeDB",
    packages=find_packages(),
    install_requires=[
        'cryptography',
        'pandas',
        'numpy',
        'pyyaml',
        'setuptools',
        'jmespath',
        'requests',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: LGPLv3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

