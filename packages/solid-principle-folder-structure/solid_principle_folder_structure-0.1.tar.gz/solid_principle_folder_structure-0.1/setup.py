from setuptools import setup, find_packages
import os
from setuptools.command.install import install


class PostInstallCommand(install):
    """Post-installation for installation mode."""

    def run(self):
        install.run(self)
        self.create_dir_structure()

    @staticmethod
    def create_dir_structure():
        base_path = ''
        dir_structure = [
            'backend/api/controller',
            'backend/client',
            'backend/config',
            'backend/custom_enum',
            'backend/dao',
            'backend/db',
            'backend/dto',
            'backend/routes',
            'backend/service/common',
            'backend/utils',
            'backend/vo'
        ]

        for directory in dir_structure:
            os.makedirs(os.path.join(base_path, directory), exist_ok=True)


setup(
    name='solid_principle_folder_structure',
    version='0.1',
    author='Tarun Mondal',
    author_email='tarunmondal114@gmail.com',
    description='A brief description of your package',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/your-repo',
    packages=find_packages(),
    include_package_data=True,
    package_data={
        '': [
            'backend/*',
            'backend/api/controller/*',
            'backend/client/*',
            'backend/config/*',
            'backend/custom_enum/*',
            'backend/dao/*',
            'backend/db/*',
            'backend/dto/*',
            'backend/routes/*',
            'backend/service/common/*',
            'backend/utils/*',
            'backend/vo/*'
        ]
    },
    cmdclass={'install': PostInstallCommand,
              },
    install_requires=[
        # your dependencies
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
