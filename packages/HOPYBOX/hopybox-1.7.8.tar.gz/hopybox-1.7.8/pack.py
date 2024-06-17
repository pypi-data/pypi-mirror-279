import os
os.system('rm -rf HOPYBOX.egg-info')
os.system('rm -rf dist')
os.system('python3 -m build --sdist')
mode = input('test or normal ?')
if mode == 'test':
  os.system('python3 -m twine upload --repository testpypi dist/*')
else:
  os.system('python3 -m twine upload dist/*')
os.system('rm -rf HOPYBOX.egg-info')
os.system('rm -rf dist')