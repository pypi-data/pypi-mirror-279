from setuptools import setup

setup(
    name='paquete-hackademy',
    description='Código fuente para publicar en PYPI el ejemplo de un paquete de calculadoras varias',
    version='1.0.0',
    author='Nataya Flores',
    url='https://github.com/natayadev/paquete-hackademy',
    download_url='https://github.com/natayadev/paquete-hackademy/tarball/1.0.0',
    install_requires=[
        'importlib-metadata; python_version == "3.12"',
    ]
)