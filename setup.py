from setuptools import setup

setup(name='aiow3parity',
      version='1.1',
      description='Easy go to parity w3 transaction',
      url='https://github.com/Js-Nanodegree/pythonEth',
      author='Js-Nanodegree',
      author_email='js-nanodegree@gmail.com',
      license='MIT',
      packages=['aiow3parity'],
      install_requires=['web3', "asyncio", "json", "aiohttp", "async_timeout"],
)
