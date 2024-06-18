from setuptools import setup, find_packages

setup(
    name='universal123',
    version='3',
    description='this sdk is a working protype',
    author='Rishabh Sharma',
    author_email='rishabhsharmabwr@gmail.com',
    packages=find_packages(),
    install_requires=[
        # Add any other dependencies here
    ],
)

#command to run setup.py
    # -> python3 setup.py sdist
#command to uplode sdk package to PyPi account
    # -> twine upload dist/*