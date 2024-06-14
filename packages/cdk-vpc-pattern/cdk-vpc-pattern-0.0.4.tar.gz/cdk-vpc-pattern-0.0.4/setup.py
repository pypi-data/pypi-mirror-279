import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "cdk-vpc-pattern",
    "version": "0.0.4",
    "description": "A CDK pattern to create a VPC with public and private subnets",
    "license": "Apache-2.0",
    "url": "https://github.com/parraletz/cdk-vpc-pattern.git",
    "long_description_content_type": "text/markdown",
    "author": "Alex Parra<parraletz@gmail.com>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/parraletz/cdk-vpc-pattern.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cdk_vpc_pattern",
        "cdk_vpc_pattern._jsii"
    ],
    "package_data": {
        "cdk_vpc_pattern._jsii": [
            "cdk-vpc-pattern@0.0.4.jsii.tgz"
        ],
        "cdk_vpc_pattern": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.8",
    "install_requires": [
        "aws-cdk-lib>=2.137.0, <3.0.0",
        "constructs>=10.3.0, <11.0.0",
        "jsii>=1.99.0, <2.0.0",
        "publication>=0.0.3",
        "typeguard~=2.13.3"
    ],
    "classifiers": [
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Typing :: Typed",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved"
    ],
    "scripts": []
}
"""
)

with open("README.md", encoding="utf8") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
