from setuptools import setup, find_packages

setup(
    name='vernam-kit',
    version='0.1',
    url='',
    license='BSD',
    author='Ilya',
    author_email='mygodishe@gmail.com',
    description=(
        'Console utilities for Vernam encryption.'
    ),
    packages=find_packages('.'),
    zip_safe=False,
    platforms='any',
    entry_points = {
        'console_scripts': [
            'vernam_decode = vernam_kit.decode:endpoint',
            'vernam_encode = vernam_kit.encode:endpoint',
            'vernam_generate = vernam_kit.generate:endpoint',
        ],
    },
)