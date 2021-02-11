from setuptools import setup, find_packages


with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="openlostcat",
    version="1.0.0",
    author="Lukács Gábor, Molnár András",
    author_email="lukacs.hod@gmail.com, molnar.andras.jozsef@gmail.com",
    description="Open Logic-based Simple Tag-bundle Categorizer",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    license="GPLv2",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=['immutabledict > 1.0.0', 'numpy', 'requests'],
    test_suite="tests",
)