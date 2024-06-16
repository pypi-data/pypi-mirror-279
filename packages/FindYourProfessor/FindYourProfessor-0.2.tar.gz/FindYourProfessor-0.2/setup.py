from setuptools import setup, find_packages

setup(
    name='FindYourProfessor',
    version='0.2',
    packages=find_packages(),
    install_requires=[
        'requests',
        'beautifulsoup4',
    ],
    entry_points={
        'console_scripts': [
            'FindYourProfessor=FindYourProfessor.scraper:main',
        ],
    },
    author='Swaranjit Roy',
    author_email='swaranjitroy08@gmail.com',
    description='A python based web scraper tool to extract emails of professors matching with keywords representing professors field of interest. It takes in the faculty directory url of a university and the keywords as input and returns the name, email and webpage of the professors with matching research interest.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Swaran66/FindProff.',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
