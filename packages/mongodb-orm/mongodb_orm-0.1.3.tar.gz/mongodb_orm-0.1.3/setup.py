from setuptools import setup, find_packages

with open("requirements.txt", "r") as f:
    requirements = f.read().splitlines()

# Fix and optimise the library installation
setup(
    name="mongodb_orm",
    version="0.1.3",
    author="Khai",
    author_email="sarraj.khaireddine@gmail.com",
    license="MIT",
    packages=find_packages(),
    include_package_data=True,
    description="mongodb ORM for django framework",
    long_description="mongodb ORM for django framework",
    install_requires=requirements,
    classifiers=[
        "License :: OSI Approved :: MIT License",
    ],
)