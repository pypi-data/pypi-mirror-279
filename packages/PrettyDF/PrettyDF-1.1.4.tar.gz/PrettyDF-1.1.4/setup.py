from setuptools import setup, find_packages
from pathlib import Path

dir = Path(__file__).parent
README = (dir / "README.md").read_text()

setup(
    name='PrettyDF',
    version='1.1.4',
    packages=find_packages(),
    author='DawnSaju',
    description='Pretty Print DataFrames',
    long_description=README,
    long_description_content_type='text/markdown',
    author_email = "dawnsajubusiness@gmail.com",
    classifiers=[
        'Programming Language :: Python :: 3'
    ],

    install_requires=[
        'pyfiglet',
        'asciimatics',
        'pandas',
        'tabulate',
        'matplotlib'
    ],
    entry_points={
        'console_scripts': [
            'PrettyDF-credits=PrettyDF.main:credits',
        ],
    },
)

