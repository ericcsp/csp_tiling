import os
import subprocess
import yaml

def list_files(**kw):
  result = subprocess.run(['az',
                         'storage',
                         'blob',
                         'list',
                         '--prefix',
                         f'{kw["src_folder"]}{kw["src_prefix"]}',
                         '--output',
                         'yaml',
                         '--account-name',
                         kw['account'],
                         '-c',
                         kw['src_container'],
                         '--account-key',
                         os.env['AZURE_ACCOUNT_KEY']], stdout=subprocess.PIPE)
  return [fil["name"] for fil in yaml.safe_load(result.stdout)]

def get_files(**kw):
  files = list_files(**kw)
  for fil in files:
    result = subprocess.run(['az',
                              'storage',
                              'blob',
                              'download',
                              '-f',
                              fil.replace(kw["src_folder"], kw["local_folder"],
                              '-n',
                              fil,
                              '--account-name',
                              kw['account'],
                              '-c',
                              kw['src_container'],
                              '--account-key',
                              os.env['AZURE_ACCOUNT_KEY']], stdout=subprocess.PIPE)
