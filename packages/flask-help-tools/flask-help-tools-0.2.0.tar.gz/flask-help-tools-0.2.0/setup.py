from setuptools import setup, find_packages

setup(
    name='flask-help-tools',
    version='0.2.0',
    author='rathe12',
    author_email='markzerone1@gmail.com',
    description='A library that provides examples and solutions for common tasks in Flask applications',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/rathe12/flask-help-tools',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[
        'Flask>=1.1.2',
    ],
)
