import setuptools

setuptools.setup(
    name = "tripawnOpen",
    version='0.1.7',
    description="Under Tacker package creation written by MitrePat",
    author="anomaly",
    author_email="anomaly@test.com",
    url="https://eu4ng.tistory.com",
    install_require=["requests"],
    packages=setuptools.find_packages(exclude=[]),
    python_requires='>=3.6',
    package_data={},
    zip_sage=False,
    classifiers=[
         'Programming Language :: Python :: 3.6',
         'Programming Language :: Python :: 3.7',
         'Programming Language :: Python :: 3.8',
    ],
)
