from setuptools import setup, find_packages


def readme():
    with open('README.md', 'r') as f:
        return f.read()


setup(
    name='ekn',
    version='0.1.4',
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'ekn': ['data/*.png', '1.txt'],  # Указываем путь к изображениям
    },
    install_requires=['requests>=2.25.1', 'Pillow'],
    classifiers=[
        'Programming Language :: Python :: 3.11',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ],
    keywords='ekn',
    python_requires='>=3.6'
)
