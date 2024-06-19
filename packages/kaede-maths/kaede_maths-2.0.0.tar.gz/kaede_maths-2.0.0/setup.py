from setuptools import setup, find_packages

setup(
    name='kaede-maths',
    version='2.0.0',
    author='Kaede Dev Kento Hinode ',
    author_email='cleaverdeath@gmail.com',
    description='A comprehensive library for mathematical operations without external dependencies',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
