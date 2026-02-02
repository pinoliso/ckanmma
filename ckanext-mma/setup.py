from setuptools import setup, find_packages

setup(
    name='ckanext-mma',
    version='0.1.0',
    description='Tema CKAN MMA',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    entry_points={
        'ckan.plugins': [
            'mma=ckanext.mma.plugin:MmaPlugin',
        ],
    },
)

