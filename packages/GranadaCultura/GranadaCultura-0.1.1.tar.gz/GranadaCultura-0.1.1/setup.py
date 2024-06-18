from setuptools import setup, find_packages

setup(
    name='GranadaCultura',
    version='0.1.1',
    description='Descripción del paquete GranadaCultura',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/lusangom/GranadaCultura',  
    author='Lucia Sanchez Montes Gomez',
    author_email='lsangom@correo.ugr.es',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[
        "numpy == 1.23.5",
        "pandas==1.5.2",
        "matplotlib==3.8.2",
        "folium==0.15.1",
        "geopandas==0.14.3",
        "osmnx==1.9.1",
    ],
   
)
