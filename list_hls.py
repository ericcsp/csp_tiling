import subprocess
import yaml
result = subprocess.run(['az',
                         'storage',
                         'blob',
                         'list',
                         '--prefix',
                         'hls_output_2021-05-13',
                         '--output',
                         'yaml',
                         '--account-name',
                         'usfs',
                         '-c',
                         'fia',
                         '--account-key',
                         '<redacted>'], stdout=subprocess.PIPE)
files = [fil["name"] for fil in yaml.safe_load(result.stdout)]

def main():
  for fil in files:
    result2 = subprocess.run(['az',
                              'storage',
                              'blob',
                              'download',
                              '-f',
                              fil,
                              '-n',
                              fil,
                              '--account-name',
                              'usfs',
                              '-c',
                              'fia',
                              '--account-key',
                              '<redacted>'], stdout=subprocess.PIPE)

if __name__ == "__main__":
  main()
