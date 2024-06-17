from setuptools import setup, find_packages

setup(
    name='myapp_CJ',
    version='1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'requests',
        # Add other dependencies here
    ],
    entry_points={
        'console_scripts': [
            'myapp-cli = myapp_CJ.cli:main',
        ],
    },
)