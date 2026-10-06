from setuptools import find_packages, setup

package_name = 'ugv_control'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', ['launch/ugv.launch.py']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='harshit',
    maintainer_email='harshitgames11@email.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'ugv_controller = ugv_control.ugv_controller:main',
        ],
    },
)
