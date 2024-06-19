from setuptools import setup, find_packages


# List of requirements
requirements = [
    'pyyaml',
    'lusid-bundle'
]




setup(
    name='lusid_express',
    version='1.2.0',
    package_dir={'': 'src'},  # tells setuptools that packages are under src
    packages=find_packages(where='src'),  # tells setuptools to look for packages in src
    install_requires=requirements,
    description='lusid-express is a python package that makes it quick and easy to get started using Lusid and Luminesce.',
    long_description=open('README.md').read(),
    include_package_data=True,  
    long_description_content_type='text/markdown',
    author='Orlando Calvo',
    author_email='orlando.calvo@finbourne.com',
    url='https://gitlab.com/finbourne/clientengineering/lusid_express',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.9',
    ],
)