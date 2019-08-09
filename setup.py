import setuptools

# with open("README.md", "r") as fh:
#     long_description = fh.read()

setuptools.setup(
    name="gd-proxygrabber",
    version="0.0.2",
    author="gagan singh",
    author_email="gaganpreet.gs007@gmail.com",
    description="Greendeck Proxy Grabber Package",
    long_description="try it",
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=['greendeck_helloworld', 'greendeck_helloworld.src', 'greendeck_helloworld.src.elasticsearch', 'greendeck_helloworld.src.mongodb'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'elasticsearch',
    ],
    include_package_data=True,
    zip_safe=False
)
