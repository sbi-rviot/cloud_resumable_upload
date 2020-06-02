import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name = 'cloud_resumable_upload',
    version = '0.1.dev0',
    author="Renaud Viot",
    author_email="renaud.viot@simply-bi.com",
    description = 'Upload documents from the cloud to the cloud without time out error.',
    long_description = long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sbi-rviot/cloud_resumable_upload",
    install_requires = ['pathlib'],
    packages=['cloud_resumable_upload'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        ],
    )

