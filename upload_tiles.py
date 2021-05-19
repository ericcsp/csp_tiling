import os
import subprocess

def upload(**kw):
    result = subprocess.run(['az',
                              'storage',
                              'blob',
                              'upload-batch',
                              '-d',
                              f'{kw["dst_container"]}/tiles_{kw["region"]}/{kw["this_yr"]}_{kw["region"]}_{kw["this_var"]}_tiles',
                              '-s',
                              kw["tilesdir"],
                              '--account-name',
                              kw['account'],
                              '--account-key',
                              os.env['AZURE_ACCOUNT_KEY']], stdout=subprocess.PIPE)

