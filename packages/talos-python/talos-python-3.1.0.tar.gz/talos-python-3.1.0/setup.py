from setuptools import find_packages, setup

setup(
    name='talos-python',
    version='3.1.0',
    author='huyumei',
    author_email='huyumei@xiaomi.com',
    maintainer='fangchengjin',
    maintainer_email='fangchengjin@xiaomi.com',
    description='talos python2 sdk',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'cffi',
        'python-snappy',
        'atomic',
        'dnspython',
        'requests',
        'futures',
        'IPy'
    ],
)

