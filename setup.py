from distutils.core import setup

setup(name='ip411',
    version='0.1.0',
    description='Locate an IP address on a map in your terminal',
    author='Cameron Ruatta',
    packages=['ip411'],
    scripts=['bin/ip411'],
    data_files=[('share/ip411', ['ip411/world.json'])],
    package_data={'ip411': ['README.md', 'LICENSE']}
)
