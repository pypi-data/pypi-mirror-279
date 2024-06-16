from setuptools import setup, find_packages

setup(
    name='filestates',
    version=open('version.txt').read(),
    author='weeger',
    author_email='contact@example.com',
    description='A tool for managing file states, with configuration files in YAML.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/weeger/filestates',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    install_requires=[
        'pyyaml',
    ],
    python_requires='>=3.6',
)
