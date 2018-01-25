from setuptools import setup

setup(
    name="echo",
    version='0.1',
    description='JIM messenger',
    long_description='Json instant messenger with presence control',
    url='https://github.com/smaskin/echo',
    license='MIT',
    keywords=['python', 'messenger', 'jim'],
    author='Sergey Maskin',
    author_email='s.maskin@mail.ru',
    packages=['src'],
    include_package_data=True,
    python_requires='>=3.5',
    install_requires=[
        'PyQt5==5.9', 'SQLAlchemy==1.1.15'
    ],
)