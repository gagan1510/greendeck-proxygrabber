import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="greendeck-proxygrabber",
    version="0.0.1",
    author="gagan singh",
    author_email="gaganpreet.gs007@gmail.com",
    description="Greendeck Proxy Grabber Package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/greendeck-libraries/gd-proxy-grabber/tree/proxy_grabber",
    packages=['greendeck_proxy', 'greendeck_proxy.src', 'greendeck_proxy.src.proxygrabber'],
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
