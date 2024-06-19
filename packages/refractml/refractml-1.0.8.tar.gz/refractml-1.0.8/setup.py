# -*- coding: utf-8 -*-
from setuptools import find_packages, setup

extras_require = {
    "vanilla": [
        "mosaic-utils==1.0.1",
    ],
    "complete-with-utils": [
        "mosaic-utils[complete]==1.0.1"
    ],
    "complete": [
        "mosaic-utils[complete]==1.0.1",
    ],
    "utils_flavours": [
        "mosaic-utils[flavours]==1.0.1",
    ],
    "utils_common": [
        "mosaic-utils[common]==1.0.1",
    ],
    "utils_metrics": [
        "mosaic-utils[metrics]==1.0.1",
    ],
    "utils_k8": [
        "mosaic-utils[k8]==1.0.1",
    ],
    "common": [
        "mosaic-utils[nb-template-serving]==1.0.1",
        "importlib-resources==5.4.0",
        "Pillow==8.4.0",
    ],
}


setup(
    name="refractml",
    package_dir={"refractml":"refractml"},
    version="1.0.8",
    description="REST API client for Refract AI",
    url="https://git.lti-aiq.in/akhil-lawrence/mosaic-ai-client",
    author="Akhil Lawrence",
    author_email="akhil.lawrence@lntinfotech.com",
    classifiers=["Programming Language :: Python :: 3.8"],
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "cloudpickle==1.6.0",
        "requests_toolbelt==1.0.0",
        "shutils==0.1.0",
        "PyYAML==6.0",
        "mosaic-utils",
        "urllib3==1.26.19",
        'numpy==1.26.4; python_version>"3.8"',
        'numpy==1.24.4; python_version<="3.8"'
    ],
    extras_require=extras_require,
)
 
