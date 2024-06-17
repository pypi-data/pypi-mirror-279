from setuptools import setup, find_packages


def readme():
  with open('README.md', 'r') as f:
    return f.read()


setup(
  name='ekn',
  version='0.0.8',
  author='damirem',
  author_email='bd-spam@mail.ru',
  description='ekn',
  long_description=readme(),
  long_description_content_type='text/markdown',
  packages=find_packages(),
  include_package_data=True,
  package_data={
      'data': ['teor/*.png', '1.txt'],  # Указываем путь к изображениям
  },
  install_requires=['requests>=2.25.1'],
  classifiers=[
    'Programming Language :: Python :: 3.11',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent'
  ],
  keywords='ekn',
  python_requires='>=3.6'
)