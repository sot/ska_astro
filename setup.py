from setuptools import setup
setup(name='Ska.astro',
      author = 'Tom Aldcroft',
      description='Astronomy utilities',
      author_email = 'aldcroft@head.cfa.harvard.edu',
      py_modules = ['Ska.astro'],
      version='0.2.2',
      zip_safe=False,
      packages=['Ska'],
      package_dir={'Ska' : 'Ska'},
      package_data={}
      )
