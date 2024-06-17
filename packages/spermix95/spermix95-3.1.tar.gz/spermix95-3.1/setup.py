

from setuptools import setup, find_namespace_packages
import os

# Ensure that every directory has an __init__.py file
for root, dirs, files in os.walk('src/smper/files'):
    for dir in dirs:
        init_file = os.path.join(root, dir, '__init__.py')
        if not os.path.exists(init_file):
            with open(init_file, 'w') as f:
                pass

setup(
    name='spermix95',
    version='3.1',
    url='https://github.com/parlorsky/sempaiper',
    license='MIT',
    author='Levap Vobayr',
    author_email='tffriend015@gmail.com',
    description='',
    packages=find_namespace_packages(where="src"),
    package_dir={"": "src"},
    package_data={
        "smper.files": ["**/*.jpg"],
    },
    zip_safe=False
)