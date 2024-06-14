from setuptools import setup,find_packages
from datetime import datetime
version='0.4.242'

setup(name='MobileInventoryCLI',
      version=version,
      author="Carl Joseph Hirner III",
      author_email="k.j.hirner.wisdom@gmail.com",
      description="modify/update/use MobileInventoryPro *.bck files",
      classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Operating System :: Android',
        'Environment :: Console',
        'Programming Language :: SQL',
          ],
      packages=find_packages(),
      python_requires='>=3.6',
      install_requires=['cython','pint','pyupc-ean','openpyxl','plyer','colored','numpy','pandas','Pillow','python-barcode','qrcode','requests','sqlalchemy','argparse','geocoder','beautifulsoup4'],
      package_data={
        '':["*.config","*.txt","*.README","*.TTF"],
        }
      )

