import setuptools
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
setuptools.setup(
    name="US_statemap",
    version="0.0.1",
    author="spcnkonno",
    author_email="nkonno@sciencepark.co.jp",
    description="Displays a map of the United States as specified",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/spcnkonno/US_statemap",
    project_urls={
        "Bug Tracker": "https://github.com/spcnkonno/US_statemap",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"":"src"},
    py_modules=['US_statemap'],
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.8.10",
    entry_points = {
        'console_scripts': [
            'US_statemap = US_statemap:main'
        ]
    },
)