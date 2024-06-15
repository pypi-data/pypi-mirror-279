from setuptools import setup, find_packages

setup(
    name='mlintern010',
    version='0.1.5',
    packages=find_packages(),
    install_requires =[
        'numpy',
        'pandas',
        'termcolor'
    ],
    entry_points={
        'console_scripts': ['mlintern-010=mlintern010:inita'],
    },
)