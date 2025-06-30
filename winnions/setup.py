from setuptools import find_packages, setup

setup(
    name="winnions",
    packages=find_packages(exclude=["winnions_tests"]),
    install_requires=[
        "dagster",
        "dagster-cloud"
    ],
    extras_require={"dev": ["dagster-webserver", "pytest"]},
)
