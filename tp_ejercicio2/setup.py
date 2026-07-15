import os
from glob import glob
from setuptools import find_packages, setup

package_name = 'tp_ejercicio2'

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
    description='Ejercicio 2: action server/client de republicado de texto',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'text_action_server = tp_ejercicio2.text_action_server:main',
            'text_action_client = tp_ejercicio2.text_action_client:main',
        ],
    },
)
