import setuptools

setuptools.setup(
    name='RabbitSpider',
    version='2.1',
    author='一纸',
    author_email='2395396520@qq.com',
    url='https://github.com/YunTom/RabbitSpider/tree/master',
    packages=['RabbitSpider', 'RabbitSpider.core', 'RabbitSpider.http', 'RabbitSpider.utils', 'RabbitSpider.templates'],
    entry_points={
        'console_scripts': [
            'rabbit = RabbitSpider.templates.__template:main',
        ],
    },
    python_requires='>=3.8',
    install_requires=[
        'aio-pika>=9.4.1',
        'curl_cffi>=0.6.2',
        'loguru>=0.7.2',
        'parsel>=1.9.1',
        'pydantic>=2.7.0',
        'redis>=5.0.3',
        'w3lib>=2.1.2',
        'chardet>=5.2.0',
        'loguru>=0.7.2',
        'chardet>=5.2.0'
    ],
)
