from setuptools import setup, find_packages

setup(
    name='mlintern010',
    version='0.1',
    packages=find_packages(),
    install_requires =[
        'numpy',
        'pandas'
    ],
    entry_points={
        "console_scripts":[
            "mlintern010 = mlintern010:intia"
        ],
    },
)