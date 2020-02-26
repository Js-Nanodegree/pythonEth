from setuptools import setup

setup(
    name='aiow3parity',
    version='0.0.1',
    description='acquire data published on the smartfact web page',
    url='https://github.com/Js-Nanodegree/pythonEth',
    author='Js-Nanodegree',
    author_email='jsnanodegree@gmail.com',
    license='MIT',
    packages=[
        'aiow3parity',
    ],
    package_data={
        'aiow3parity': [
            'resources/20160703_233149/*.data',
            'resources/20160703_233149_broken_fsc/fsc.data',
        ]
    },
    install_requires=[
        'web3', "asyncio", "aiohttp", "async_timeout"
    ],
    zip_safe=True,
)