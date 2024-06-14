from setuptools import setup

setup(
    name='Condate',  # Имя вашего пакета
    version='0.1',  # Версия вашего пакета
    py_modules=['condate'],  # Список модулей, включаемых в пакет
    author='Avinion',  # Имя автора
    author_email='shizofrin@gmail.com',  # Email автора
    url='https://twitter.com/Lanaev0li',  # URL проекта
    license='Avinion Group',  # Лицензия
    description='A simple date conversion script',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'condate=condate:convert_date',  # 'condate' - это имя команды, которая будет создана
        ],
    },
)
