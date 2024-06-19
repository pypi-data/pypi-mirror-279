from setuptools import setup
from zlicutils import __version__

setup(name='zlicutils',
      version=__version__,
      description='A library for shared classes and functionalities in the ZLiC project.',
      url='https://github.com/dfriedenberger/zlic-tools.git',
      long_description=open('README.md', encoding="UTF-8").read(),
      long_description_content_type='text/markdown',
      author='Dirk Friedenberger',
      author_email='projekte@frittenburger.de',
      license='GPLv3',
      packages=['zlicutils'],
      install_requires=['fastapi', 'uvicorn'],
      classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
        'Operating System :: OS Independent',
      ],
      zip_safe=False)
