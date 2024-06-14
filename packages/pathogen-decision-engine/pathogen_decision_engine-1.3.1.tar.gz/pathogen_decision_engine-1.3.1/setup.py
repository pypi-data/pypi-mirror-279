from setuptools import setup, find_packages
import os


def read_file(filename):
    with open(os.path.join(os.path.dirname(__file__), filename)) as file:
        return file.read()


setup(
    name='pathogen-decision-engine',
    version='1.3.1',
    long_description=read_file('README.md'),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=[
        'pandas>=2.0.3',
        'rule_engine'
    ],
    entry_points={
        'console_scripts': [
            'decision_engine_cli = pathogen_decision_engine.decision_engine_cli:main'
        ]
    }
)
