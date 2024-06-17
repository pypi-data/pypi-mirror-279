import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="anaspro",
    version="1.0.0",
    author="Anas Pro",
    author_email="anaspro@example.com",
    description="A library to generate random user data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/xxxxx/anaspro",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'Faker>=9.0.0'
    ],
    package_data={
        'anaspro': ['data/countries.json'],
    },
    include_package_data=True,
)

