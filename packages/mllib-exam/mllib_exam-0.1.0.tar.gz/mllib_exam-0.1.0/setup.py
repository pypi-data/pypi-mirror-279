from setuptools import setup, find_packages

libs = open("requirements.txt").read().splitlines()
setup(
    name="mllib_exam",  # Название библиотеки
    version="0.1.0",  # Версия библиотеки
    license="MIT",  # Тип лицензии
    author="VS",  # Автор
    zip_safe=False,  # False - устанавливать как папку
    platforms=["any"],  # Какие платформы поддерживает
    packages=find_packages(),
    package_data={
        # Указываем пакеты и соответствующие шаблоны файлов
        "econom": ["src/*.yaml"],
    },
    install_requires=libs,  # Библиотеки которые надо установить
    # Если надо, можно указать версию
    test_suite="nose.collector",  # Какой инструмент запускать для тестирования
)
