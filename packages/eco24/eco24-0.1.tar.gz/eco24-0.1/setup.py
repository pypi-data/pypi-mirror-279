from setuptools import setup, find_packages

libs = open("requirements.txt").read().splitlines()
setup(
    name="eco24",  # Название библиотеки
    version="0.1",  # Версия библиотеки
    license="MIT",  # Тип лицензии
    author="VS",  # Автор
    zip_safe=False,  # False - устанавливать как папку
    platforms=["any"],  # Какие платформы поддерживает
    packages=find_packages(),
    setup_requires=libs,  # Библиотеки которые надо установить
    # Если надо, можно указать версию
    test_suite="nose.collector",  # Какой инструмент запускать для тестирования
)
