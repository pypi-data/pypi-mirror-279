from setuptools import setup, find_packages

setup(
    name='rentavle_sdk',
    version='0.1.3',
    packages=find_packages(),
    install_requires=[
        'requests>=2.25.0'
    ],
    author='Rentavle',
    author_email='supergravitycorp@gmail.com',
    description='A simple SDK for the Rentavle service',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/rentavle/rentavle-sdk-python',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
