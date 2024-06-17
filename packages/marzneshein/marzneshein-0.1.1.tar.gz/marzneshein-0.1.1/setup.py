from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='marzneshein',
    version='0.1.1',
    description='Marzneshein Control API Client',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Artem',
    author_email='contact@sm1ky.com',
    url='https://github.com/sm1ky/marzneshein_api',
    packages=find_packages(),
    install_requires=[
        'httpx',
        'pydantic',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',
)