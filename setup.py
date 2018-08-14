from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='usercheck',
    version='1.0',
    packages=['usercheck', 'usercheck.services'],
    url='https://github.com/ethanquix/userchecker',
    license='MIT',
    author='Dimitri Wyzlic',
    author_email='dimitriwyzlic@gmail.com',
    description='Check if your username is taken from various sites',
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[
   'requests'
    ],

    include_package_data=True,
    entry_points={
        'console_scripts': [
            'usercheck=usercheck:main',
        ],
    },

)
