import setuptools

setuptools.setup(
    name="alida-dataset",
    version="0.0.5",
    author="Alida research team",
    author_email="engineering-alida-lab@eng.it",
    description="Utils for loading datasets using alida services.",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires = [
        #"hdfs>=2.0.0",
        "bda-service-utils",
        "s3fs",
        "minio",
        "alida-arg-parser",
        "boto",
        "ds-io-utilities",
        "kafka-python"
        ],
)
