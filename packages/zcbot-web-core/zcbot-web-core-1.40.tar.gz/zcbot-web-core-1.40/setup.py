from distutils.core import setup
from setuptools import find_packages

with open('README.rst', 'r') as f:
    long_description = f.read()

setup(name='zcbot-web-core',
      version='1.40',
      description='zcbot web core for zsodata',
      long_description=long_description,
      author='zsodata',
      author_email='team@zso.io',
      url='http://www.zsodata.com',
      install_requires=[
            # "fastapi==0.109.2",
            # "starlette==0.36.3",
            # "uvicorn==0.27.1",
            # "click==8.1.7",
            # "h11==0.14.0",
            # "pydantic==1.8.2",
            # "python-dotenv==0.19.0",
            # "python-multipart==0.0.5",
            # "six==1.16.0",
            # "tzlocal==2.1",
            # "pandas==1.0.5",
            # "httpx==0.26.0",
            # "httpx-socks==0.8.1",
            # "requests==2.31.0",
            # "numpy==1.22.3",
            # "pymongo==3.11.0",
            # "redis==3.5.3",
            # "python-dateutil==2.8.2",
            # "pytz==2024.1",
            # "tenacity==8.2.3",
            # "cryptography==42.0.4",
            # "APScheduler==3.10.4",
            # "oss2==2.12.1",
      ],
      python_requires='>=3.7',
      license='BSD License',
      packages=find_packages(),
      platforms=['all'],
      include_package_data=True
      )
