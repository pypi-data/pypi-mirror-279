from setuptools import setup, find_packages

setup(
    name='hexon_mini',
    version='0.1.1',
    packages=find_packages(),
    install_requires=[
        'websocket-client',
    ],
    tests_require=[
        'unittest',
    ],
    include_package_data=True,
    license='MIT',
    description='A WebSocket client for controlling the HEXON MINI robotic arm.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://arixarobotics.com',  # Replace with your URL
    author='ARIXA Robotics',
    author_email='arixa.robotics@gmail.com',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
