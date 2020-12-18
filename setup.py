from setuptools import setup, find_packages

readme = open('README.md').read()
requirements_list = [pkg for pkg in open('requirements.txt').readlines()]

setup(
    name='cp_request',
    version='0.0.1',
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    install_requires=requirements_list,

    author='Ben Keller',
    author_email='bjkeller@uw.edu',
    description='Package for experimental requests',
    license='MIT',
    long_description=readme,
    project_urls={
        'Source Code': 'https://github.com/SD2E/cp-request-api'
    }
)
