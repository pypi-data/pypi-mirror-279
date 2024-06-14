from setuptools import setup, find_packages
import os

# Текст лицензии Avinion Group
LICENSE_TEXT = """
Avinion Group
"""

# Директория проекта
PROJECT_DIR = os.path.abspath(os.path.dirname(__file__))

setup(
    name='aovervid',  # Название вашего проекта
    version='0.1',  # Версия вашего проекта
    packages=find_packages(),  # Поиск всех пакетов
    install_requires=[
        # Здесь можно указать зависимости
    ],
    entry_points={
        'console_scripts': [
            'aovervid = overlay_audio.aovervid:main',  # Укажите правильный путь к вашему скрипту
        ],
    },
    author='Avinion',  # Автор вашего проекта
    author_email='shizofrin@gmail.com',
    description='Скрипт для замены и наложения аудио на видео.',
    url='https://twitter.com/Lanaev0li',  # URL вашего репозитория
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: Other/Proprietary License',  # Здесь указывается лицензия
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    license=LICENSE_TEXT,  # Текст лицензии Avinion Group
    long_description=open(os.path.join(PROJECT_DIR, 'README.md')).read(),
    long_description_content_type='text/markdown',
)
