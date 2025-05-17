from setuptools import find_packages, setup

setup(
    name="DAGSTER_HOME",
    packages=find_packages(exclude=["my_dagster_project_tests"]),
    install_requires=[
        "dagster",
        "dagster-cloud",
        "google-generativeai",
        "requests",
        "b2sdk",
        "pinecone",
        "aiohttp",
        "beautifulsoup4",
        "tenacity",
        "lxml"
    ],
    extras_require={"dev": ["dagster-webserver", "pytest"]},
)
