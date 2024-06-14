# coding: utf-8

"""
    iparapheur

    iparapheur v5.x main core application.  The main link between every sub-services, integrating business code logic. 

    The version of the OpenAPI document: DEVELOP
    Contact: iparapheur@libriciel.coop
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from setuptools import setup, find_packages  # noqa: H301

# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools
NAME = "iparapheur-provisioning"
VERSION = "1.11.7"
PYTHON_REQUIRES = ">=3.7"
REQUIRES = [
    "urllib3 >= 1.25.3, < 2.1.0",
    "python-dateutil",
    "pydantic >= 2",
    "typing-extensions >= 4.7.1",
]

setup(
    name=NAME,
    version=VERSION,
    description="iparapheur",
    author="Libriciel SCOP",
    author_email="iparapheur@libriciel.coop",
    url="",
    keywords=["OpenAPI", "OpenAPI-Generator", "iparapheur"],
    install_requires=REQUIRES,
    packages=find_packages(exclude=["test", "tests"]),
    include_package_data=True,
    license="Affero GPL 3.0",
    long_description_content_type='text/markdown',
    long_description="""\
    iparapheur v5.x main core application.  The main link between every sub-services, integrating business code logic. 
    """,  # noqa: E501
    package_data={"iparapheur_provisioning": ["py.typed"]},
)
