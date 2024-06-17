from setuptools import setup, find_packages

setup(
    name='clima',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'requests',
        'pandas',
    ],
    description='Paquete para obtener datos climatológicos de AEMET',
    author='David',
    author_email='dcortes@nexmachina.com',
    url='https://github.com/DcortesNexmachina/Climaemet',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
