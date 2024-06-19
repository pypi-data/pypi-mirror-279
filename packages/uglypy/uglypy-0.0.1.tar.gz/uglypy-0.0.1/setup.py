from setuptools import setup, find_packages

setup(
    name='uglypy',
    version='0.0.1',
    packages=find_packages(include=['uglypy', 'uglypy.*']),
    install_requires=[
        'feedparser',
        'pyyaml',
        'openai',
        'scikit-learn',
        'requests',
        'numpy',
        'tqdm',
        'spacy',
        'nltk',
        'beautifulsoup4',
        'xmltodict'
    ],
    entry_points={
        'console_scripts': [
            'uglypy=uglypy.cli:main'
        ]
    },
    author='Fabrizio Salmi',
    author_email='fabrizio.salmi@gmail.com',
    description='UglyPy - A Python package for retrieving, aggregating, and processing RSS feeds.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/fabriziosalmi/UglyFeed',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)

