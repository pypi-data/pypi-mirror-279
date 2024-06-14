import setuptools

# Display a message during installation
print("Installing pynumint...")

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pynumint",
    version="0.1.7",
    author="Arjun Jagdale",
    author_email="arjunjagdale14@gmail.com",
    description="pynumint is a package for Numerical Integration tasks",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/CodeSleuthX/pynumint",
    packages=setuptools.find_packages(where='pynumint/src'),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ],
    keywords="numerical integration mathematics science",
    python_requires='>=3.6',
    py_modules=["pynumint"],
    package_dir={'': 'pynumint/src'},
    install_requires=[
        # Example dependencies
	"numpy>=1.18.0",

    ],
    extras_require={
        'dev': [
            'check-manifest',
            'flake8',
        ],
        'test': [
            'coverage',
        ],
    },

    project_urls={
        'Bug Reports': 'https://github.com/CodeSleuthX/pynumint/issues',
        'Source': 'https://github.com/CodeSleuthX/pynumint',
    },
)

# Print a completion message
print("pynumint has been successfully installed!")
