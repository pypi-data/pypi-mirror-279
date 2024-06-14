# -*- coding: utf-8 -*-
"""
@author: Vault-of-Procrastination
"""

# In[0]

from setuptools import setup, find_packages

# In[1]

readme = open('./README.md').read()

requires = [x.strip() for x in open('requirements.txt').readlines() if x.strip()]

# In[2]

setup(name = 'Multiprocessing_gRPC_Load_Balancer',
      version = '0.0.1',
      description = 'Its a Load Balancer for multiprocessing gRPC Servers.',
      long_description = readme,
      long_description_content_type = 'text/markdown',
      author = 'Vault-of-Procrastination',
      author_email = 'vault_of_procrastination@outlook.com',
      maintainer = 'Vault-of-Procrastination',
      maintainer_email = 'vault_of_procrastination@outlook.com',
      url = 'https://github.com/Vault-of-Procrastination/Multiprocessing_gRPC_Load_Balancer',
      download_url = 'https://github.com/vault-of-procrastination/Multiprocessing_gRPC_Load_Balancer/tarball/0.0.1',
      license = 'Apache Software License 2.0',
      keywords = 'grpc load balancer multiprocessing prometheus monitoring',
      packages = find_packages(include = ['Multiprocessing_gRPC_Load_Balancer'], exclude = ['proto_test']),
      python_requires = '>=3.12',
      install_requires = requires,
      
      classifiers=['Development Status :: 4 - Beta',
                   'Intended Audience :: Developers',
                   'Operating System :: POSIX :: Linux',
                   'Programming Language :: Python :: 3',
                   'Programming Language :: Python :: 3.12',
                   'Topic :: Communications',
                   'Topic :: System :: Monitoring',
                   'Topic :: Software Development :: Libraries',
                   'Topic :: Software Development :: Libraries :: Python Modules',
                   'License :: OSI Approved :: Apache Software License'])


