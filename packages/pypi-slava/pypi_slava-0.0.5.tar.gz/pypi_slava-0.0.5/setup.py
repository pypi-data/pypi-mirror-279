from setuptools import setup, find_packages

setup(
    name="pypi-slava",
    version="0.0.5",
    description="test tool",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author="Viacheslav Shneidmillier",
    author_email="v.shneidmiller@gmail.com",
    url="https://github.com/vshneidmiller/pypi",
    # When your source code is in a subdirectory under the project root, e.g.
    # `src/`, it is necessary to specify the `package_dir` argument.
    package_dir={"": "src"},  # Optional
    # You can just specify package directories manually here if your project is
    # simple. Or you can use find_packages().
    #
    # Alternatively, if you just want to distribute a single Python file, use
    # the `py_modules` argument instead as follows, which will expect a file
    # called `my_module.py` to exist:
    #
    #   py_modules=["my_module"],
    #
    packages=find_packages(where="src"),  # Required

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
    # Entry points. The following would provide a command called `sample` which
    # executes the function `main` from this package when invoked:
    entry_points={  # Optional
        "console_scripts": [
            "sample=sample:main",
        ],
    },
    python_requires='>=3.6',
)
