import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="greendeck-proxygrabber",
    version="0.0.9",
    author="gagan singh",
    author_email="gaganpreet.gs007@gmail.com",
    description="Greendeck Proxy Grabber Package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gagan1510/greendeck-proxygrabber",
    packages=['greendeck_proxygrabber', 'greendeck_proxygrabber.src', 'greendeck_proxygrabber.src.proxygrabber'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'lxml',
    ],
    include_package_data=True,
    zip_safe=False
)