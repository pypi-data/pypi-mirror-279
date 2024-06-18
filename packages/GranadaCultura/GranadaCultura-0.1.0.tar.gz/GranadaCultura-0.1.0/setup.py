from setuptools import setup, find_packages

setup(
    name='GranadaCultura',
    version='0.1.0',
    description='Descripción del paquete GranadaCultura',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/lusangom/GranadaCultura',  # Reemplaza con tu URL
    author='Lucia Sanchez Montes Gomez',
    author_email='lsangom@correo.ugr.es',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    
)
