import setuptools

with open("ccrp/version") as f:
    version = f.read().strip()

setuptools.setup(
    name="ccrp",
    version=version,
    author="Aapeli Vuorinen",
    description="Python library for cheap receipt printers",
    package_dir={"": "."},
    packages=setuptools.find_packages(where="."),
    package_data={"ccrp": ["version"]},
    python_requires=">=3.9",
    url="https://github.com/aapeliv/ccrp",
    classifiers=[
        "License :: OSI Approved :: MIT License",
    ],
    install_requires=[
        "pyusb",
    ],
)
