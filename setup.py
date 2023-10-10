import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    version                       = "0.1.0"               , # change this on every release
    name                          = "osbot_lambdas"  ,

    author                        = "Dinis Cruz",
    author_email                  = "dinis.cruz@owasp.org",
    description                   = "OWASP Security Bot - Lambdas",
    long_description              = long_description,
    long_description_content_type = " text/markdown",
    url                           = "https://github.com/pbx-gs/OSBot-Lambdas",
    packages                      = setuptools.find_packages(),
    classifiers                   = [ "Programming Language :: Python :: 3"   ,
                                      "License :: OSI Approved :: MIT License",
                                      "Operating System :: OS Independent"   ])