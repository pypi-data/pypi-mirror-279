from setuptools import setup, find_packages

setup(
    name='ThiagoPy',
    version='0.5',
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'ThiagoPy': ['__init__.py','microstates.py', 'microstates.jl'],
    },
    install_requires=[
        'julia',
    ],
    author='Jorge Vinicius Malosti da Silveira',
    author_email='jorge.malosti@outlook.com',
    description='Uma biblioteca Python que usa funções Julia',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    #url='https://github.com/seuusuario/mypackage',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
