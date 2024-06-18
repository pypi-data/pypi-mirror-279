from setuptools import setup, find_packages


def read_version():
    with open("VERSION", "r") as version_file:
        return version_file.read().strip()
    

setup(
    name='heroes_ai_handler',
    # version = "0.2.6",
    version = read_version(),
    packages = find_packages(),
    install_requires = [
        'undetected-chromedriver',
        'langdetect',
        'python-docx',
        'requests',
        'PyMuPDF',
        'pyodbc',
        'weaviate-client',
        'tiktoken',
        'langchain',
        'azure-storage-blob',
        'beautifulsoup4',
    ],
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