from setuptools import find_packages, setup

with open('README.md', 'r') as f:
    readme = f.read()

setup(
    name='blosc_reader',
    version='0.1.0',
    packages=find_packages(where="src"),
    url='https://github.com/syedalimohsinbukhari/blosc_reader',
    license='MIT',
    author='Syed Ali Mohsin Bukhari',
    author_email='syedali.b@outlook.com',
    description='A simple and dirty `blosc_reader` file reader and plotter.',
    long_description=readme,
    long_description_content_type="text/markdown",
    python_requires=">3.9",
    install_requires=["blosc==1.11.1", "matplotlib==3.8.4", "setuptools==70.0.0"],
    include_package_data=True,
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.9"
    ],
    entry_points={
        "console_scripts": [
            "blosc_reader = blosc_reader.blosc_reader:blosc_reader"
        ]
    }
)
