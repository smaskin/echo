from setuptools import setup

setup(
    name="echo-messenger",
    version='0.3',
    description='JIM messenger',
    long_description='Json instant messenger with presence control',
    url='https://github.com/smaskin/echo',
    license='MIT',
    keywords=['python', 'messenger', 'jim'],
    author='Sergey Maskin',
    author_email='s.maskin@mail.ru',
    packages=['echo', 'echo/helpers', 'echo/db', 'echo/log', 'echo/ui'],
    package_data={'': ['client.ui']},
    include_package_data=True,
    python_requires='>=3.5',
    install_requires=[
        'PyQt5==5.9', 'SQLAlchemy==1.1.15'
    ],
)