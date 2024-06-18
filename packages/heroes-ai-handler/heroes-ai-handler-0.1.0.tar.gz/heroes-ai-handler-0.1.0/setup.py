from setuptools import setup, find_packages

setup(
    name='heroes-ai-handler',
    version='0.1.0',
    author='Stefan Jansen',
    author_email='stefan.jansen@heroes.nl',
    description='A short description of your package',
    long_description='A longer description of your package',
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/your-package',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',
    install_requires=[
        # Add any dependencies your package needs to run
    ],
)