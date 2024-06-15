from setuptools import setup, find_packages

setup(
    name='typerux',
    version='1.0.3',
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    include_package_data=True,
    install_requires=[
        'curses-menu',
    ],
    entry_points={
        'console_scripts': [
            'typerux = typerusx.typing_1:main',
        ],
    },
)
