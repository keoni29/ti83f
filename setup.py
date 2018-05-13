from setuptools import setup

setup(name='ti83f',
      version='0.2.1',
      description='Encode and decode TI83F files',
      url='',
      author='Koen van Vliet',
      author_email='8by8mail@gmail.com',
      license='MIT',
      packages=['ti83f'],
      entry_points={
            'console_scripts': ['to8xv=ti83f.to8xv:main']},
      zip_safe=False,
      )