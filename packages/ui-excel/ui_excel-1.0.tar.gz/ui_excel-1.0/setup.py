from setuptools import setup, find_packages

setup(
    name='ui_excel',
    version='1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'requests','tkinter','flask'
        # Add other dependencies here
    ],
    entry_points={
        'console_scripts': [
            'ui_excel-cli = ui_excel.cli:main',
        ],
    },
)