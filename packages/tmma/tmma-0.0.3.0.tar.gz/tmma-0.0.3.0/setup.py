import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="tmma",
    version="0.0.3.0",
    author="Rinaldi Polese Petrolli",
    author_email="rinaldipp@gmail.com",
    description="Transfer Matrix Models for modeling acoustic treatments",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jvcarli/tmma",
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=['numpy', 'scipy', 'matplotlib', 'pandas', 'mpmath', 'xlsxwriter', 'h5py'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
