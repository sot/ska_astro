from setuptools import setup
setup(name='Ska.astro',
      author = 'Tom Aldcroft',
      description='Astronomy utilities',
      author_email = 'aldcroft@head.cfa.harvard.edu',
      py_modules = ['Ska.astro'],
      version='0.02',
      zip_safe=False,
      namespace_packages=['Ska'],
      packages=['Ska'],
      package_dir={'Ska' : 'Ska'},
      package_data={}
      )
