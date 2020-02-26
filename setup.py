from setuptools import setup

setup(name='aiow3parity',
      version='1.1',
      description='Easy go to parity w3 transaction',
      url='https://github.com/Js-Nanodegree/pythonEth',
      author='Js-Nanodegree',
      author_email='js-nanodegree@gmail.com',
      license='MIT',
      packages=['aiow3parity'],
      install_requires=[],
)
setup(
    name='aiow3parity',
    version='0.6.4',
    description='acquire data published on the smartfact web page',
    url='https://github.com/Js-Nanodegree/pythonEth',
    author='Dominik Neise, Sebastian Mueller, Maximilian Nöthe',
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
        'web3', "asyncio", "json", "aiohttp", "async_timeout"
    ],
#     tests_require=['pytest>=3.0', 'freezegun'],
#     setup_requires=['pytest-runner'],
    zip_safe=True,
)