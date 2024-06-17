from setuptools import setup, find_packages


VERSION = '0.0.1'
DESCRIPTION = 'Interact with your Dataverse'
LONG_DESCRIPTION = 'A package that allows you to perform various CRUD operations on your Dataverse'

setup(
    name="dvapi",
    version=VERSION,
    author="Kasap (Petar Kasapinov)",
    author_email="<pkasapinov@otcfin.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'api', 'crud', 'dataverse'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
