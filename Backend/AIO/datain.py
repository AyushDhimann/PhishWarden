import subprocess

url = 'http://data.phishtank.com/data/online-valid.csv'

subprocess.run(['wget', url])