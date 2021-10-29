from setuptools import setup

def readme():
    with open('README.md') as file:
        README = file.read()
    return README


setup(
    name = 'ezcord',
    version = '0.0.1',
    description = 'API wrapper for Discord',
    long_description = readme(),
    long_description_content_type="text/markdown",
    package_dir={'ezcord': 'src'},
    packages=['ezcord'],
    install_requires = [
        'aiohttp','asyncio'
    ],
    url = 'https://github.com/jnsougata/Ezcord',
    project_urls={
        "Bug Tracker": "https://github.com/jnsougata/Ezcord/issues"
    },
    author = 'Zen',
    license = 'MIT',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    python_requires=">=3.7"
)