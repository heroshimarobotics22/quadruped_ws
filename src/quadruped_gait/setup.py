from setuptools import find_packages, setup

package_name = 'quadruped_gait'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='rithvik',
    maintainer_email='rithvik@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
	'walk_gait = quadruped_gait.walk_gait:main',
	'one_leg_gait = quadruped_gait.one_leg_gait:main',
        ],
    },
)
