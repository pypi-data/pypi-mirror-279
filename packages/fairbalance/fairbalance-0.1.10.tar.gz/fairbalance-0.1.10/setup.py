import setuptools

with open("README.md", "r", encoding = "utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "fairbalance",
    version = "0.1.10",
    author = "Pierre-Antoine Lequeu @ Fujitsu Luxembourg",
    author_email = "pierre-antoine.lequeu@fujitsu.com",
    description = "bias mitigation by balancing target and/or protected attributes using resampling techniques",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    packages = setuptools.find_packages(),
    install_requires=[
        'folktables>=0.0.12',
        'imbalanced_learn==0.9.1',
        'numpy>=1.24.3',
        'pandas==2.0.3',
        'scikit_learn==1.3.2',
        'ucimlrepo==0.0.3'
    ]
)