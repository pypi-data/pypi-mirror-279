from setuptools import setup, find_packages

setup(
    name='locobuzz_python_configuration',
    version='0.1.2',
    packages=find_packages(),
    install_requires=[
        'jsonschema',
    ],
    author='Sheikh Muhammed Shoaib',
    author_email='shoaib.sheikh@locobuzz.com',
    description='A configuration builder package',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/LocoBuzz-Solutions-Pvt-Ltd/locobuzz_python_configuration',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.9',
)
