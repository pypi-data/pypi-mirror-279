from setuptools import setup, find_packages

setup(
    name='mlintern010',
    version='0.5.1',
    packages=find_packages(),
    author='R Kiran Kumar Reddy',
    author_email='rkirankumarreddy599@gmail.com',
    description='This is a package for data preprocessing',
    install_requires =[
        'numpy',
        'pandas',
        'termcolor',
        'matplotlib',
    ],
    entry_points={
        'console_scripts': ['mlintern-010=mlintern010:About.intern'],
    },
)