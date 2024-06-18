from setuptools import setup, find_packages


setup(
    name='heroes-ai-handler',
    version = "0.0.6",
    packages = find_packages(),
    install_requires = [],
    include_package_data = True,
    description = "A package for handling GPT, embeddings, and data for an AI Assistant.",
    long_description = open("README.md").read(),
    long_description_content_type = "text/markdown",
    url = "https://pypi.org/project/heroes-ai-handler/",
    author = "Stefan Jansen",
    author_email = 'stefan.jansen@heroes.nl',
    license = "MIT",
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires = '>=3.10',
)