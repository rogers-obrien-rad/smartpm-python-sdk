from setuptools import setup, find_packages

setup(
    name='smartpm_sdk',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'requests',
    ],
    author='Hagen Fritz',
    author_email='hfritz@r-o.com',
    description='A Python SDK for interacting with the SmartPM API',
    url='https://github.com/rogers-obrien-rad/smartpm-python-sdk',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Apache',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
