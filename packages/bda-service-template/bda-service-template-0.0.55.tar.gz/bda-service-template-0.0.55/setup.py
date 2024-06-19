import setuptools

setuptools.setup(
    name="bda-service-template",
    version="0.0.55",
    author="Alida research team",
    author_email="engineering-alida-lab@eng.it",
    description="Bda templates to build python services for Alida",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires = [
        "file-io-utilities",
        "ds-io-utilities",
        # "pyspark-utilities>=0.0.28",
        "bda-service-utils>=0.0.13",
        "kafka-python>=2.0.2",
        #"pyarrow>=6.0.0",
        "alida-arg-parser>=0.0.43",
        "pandas",
        "alida-dataset"
        ],
)
