from setuptools import setup, find_packages

setup(
    name='calendario_colombiano',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[],
    description='Biblioteca para manejar el calendario colombiano con festivos y fechas especiales',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Marco Eduar Serna Lopez',
    author_email='marcoesernal@gmail.com',
    url='https://github.com/MarkSerna/calendario_colombiano',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
