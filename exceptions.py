from setuptools import setup, find_packages


setup(
    name='exception_set',
    packages=find_packages()
)


class PractikumApiNotOKException(Exception):
    """Ошибка возникает в случае недоступности апи Практикума."""

    pass
