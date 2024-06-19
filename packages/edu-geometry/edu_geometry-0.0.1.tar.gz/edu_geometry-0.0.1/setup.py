from setuptools import setup, find_packages

setup(
    name="edu_geometry",
    version="0.0.1",
    packages=find_packages(),
    install_requires=[],
    description='A simple Python library for calculating the area and perimeterof geometric shapes.',
    author='Liuardo',

    # For tests
    test_suite='tests',
    tests_require=[],
    setup_requires=[]
)