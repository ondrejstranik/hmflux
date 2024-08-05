import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="hmflux",
    version="0.0.1",
    author="OndrejStranik",
    author_email="ondra.stranik@gmail.com",
    description="package to control holomin flux microscope",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ondrejstranik/hmflux",
    packages = setuptools.find_packages(),
    install_requires = [
        'pylablib',
        'keyboard',
        'microscope'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
)