from setuptools import setup, find_packages


with open('README.md') as _f:
    desc: str = _f.read()

setup(
    name='tooltils',
    description='A lightweight python utility package built on the standard library',
    long_description=desc,
    python_requires='>=3.7',
    license='MIT License',
    author='feetbots',
    author_email='pheetbots@gmail.com',
    packages=find_packages(exclude=['*tests*', '*.tests', '*.tests.*', 'tests.*', 'tests']),
    ext_modules=[],
    requires=[],
    test_suite='tests',
    include_package_data=True
)
