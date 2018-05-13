from setuptools import setup

setup(name='to8xv',
      version='0.1',
      description='Convert any file to ti8x appVar',
      url='',
      author='Koen van Vliet',
      author_email='8by8mail@gmail.com',
      license='MIT',
      packages=['to8xv'],
      entry_points={
            'console_scripts': ['to8xv=to8xv.to8xv:main']},
      zip_safe=False,
      )