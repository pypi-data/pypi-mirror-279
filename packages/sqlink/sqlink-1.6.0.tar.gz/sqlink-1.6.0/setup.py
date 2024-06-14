import setuptools

with open("README_pypi.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="sqlink",
    version="1.6.0",
    author="NanHaiLoong",
    author_email="nanhai@163.com",
    description="a efficient and concise sql framework.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitee.com/darlingxyz/sqlink",
    packages=['sqlink'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)



