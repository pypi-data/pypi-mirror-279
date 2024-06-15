from setuptools import setup

setup(name='cellworld_belief',
      author='German Espinosa',
      author_email='germanespinosa@gmail.com',
      long_description=open('./cellworld_belief/README.md').read() + '\n---\n<small>Package created with Easy-pack</small>\n',
      long_description_content_type='text/markdown',
      packages=['cellworld_belief'],
      install_requires=['cellworld_game', 'torch'],
      license='MIT',
      include_package_data=True,
      version='0.0.29',
      zip_safe=False)
