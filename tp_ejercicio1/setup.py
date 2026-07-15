import os
from glob import glob
from setuptools import find_packages, setup

package_name = 'tp_ejercicio1'

setup(
    name=package_name,
    version='0.0.1',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'),
            glob(os.path.join('launch', '*.launch.py'))),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Paulo Cesar Libreros Fajardo',
    maintainer_email='plibreros.ext@fi.uba.ar',
    description='Ejercicio 1: nodo contador con servicio de reset',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'counter_publisher = tp_ejercicio1.counter_publisher:main',
            'counter_subscriber = tp_ejercicio1.counter_subscriber:main',
        ],
    },
)
