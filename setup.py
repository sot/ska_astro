from setuptools import setup
setup(name='Ska.astroutil',
      author = 'Tom Aldcroft',
      description='Astronomy utilities',
      author_email = 'aldcroft@head.cfa.harvard.edu',
      py_modules = ['Ska.astroutil'],
      version='0.01',
      zip_safe=False,
      namespace_packages=['Ska'],
      packages=['Ska'],
      package_dir={'Ska' : 'Ska'},
      package_data={}
      )
