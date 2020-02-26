from setuptools import setup

setup(name='aiow3parity',
      version='0.1',
      description='Easy go to parity w3 transaction',
      url='',
      author='Js-Nanodegree',
      author_email='js-nanodegree@gmail.com',
      license='MIT',
      packages=['aiow3parity'],
      install_requires=['web3', "asyncio", "json", "aiohttp", "async_timeout"],
)
