import setuptools
from setuptools import setup,  find_packages

setup(
    name="pysideapi",
    packages=['jira','jira.producer','jira.model','jira.utils','jira.commons','jira.api_client',
        'dictamen','dictionary'],
    include_package_data=True,
    version="0.0.6",
    license = "MIT",
    description= "Paquete que me permite trabajar con jira, dicccionario y dictamen",
    author="Jhon Castro",
    author_email= "jhoncc20@gmail.com",
    install_requires=['requests','pytz'],
    classifiers = ["Programming Language :: Python :: 3"]

)
