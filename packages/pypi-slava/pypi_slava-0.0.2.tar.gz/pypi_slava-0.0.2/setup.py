from setuptools import setup, find_packages

setup(
    name="pypi-slava",
    version="0.0.2",
    description="test tool",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author="Viacheslav Shneidmillier",
    author_email="v.shneidmiller@gmail.com",
    url="https://github.com/vshneidmiller/pypi",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "requests",
        "PyYAML",
        "robotframework"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': [
            'pypi-slava=main:main',
        ],
    },
    python_requires='>=3.6',
)
