# -*- coding: utf-8 -*-

from setuptools import setup, distutils, Extension
import sys

if sys.version_info < (3, 7):
    sys.exit('Sorry, Python < 3.7 is not supported. Please install Python 3.7 or upwards and try again.')

platform = distutils.util.get_platform()
if "win" in platform:
    package_data = {'': ['EULA.pdf', 'requirements.txt'],
                    'lib_robot': ['lib_robot/animus_robot.dll', 'lib_robot/animus_robot.lib',
                                  'lib_robot/libwinpthread-1.dll', 'lib_robot/EULA.pdf']}
    extra_link_args = None
else:
    package_data = {'': ['EULA.pdf', 'requirements.txt'],
                    'lib_robot': ['lib_robot/libanimus_robot.so', 'lib_robot/EULA.pdf']}
    if "mac" in platform:
        extra_link_args = ["-Wl,-rpath", "-Wl,@loader_path/"]
    else:
        extra_link_args = ['-Wl,-rpath,$ORIGIN']


animus_robot_py3 = Extension('lib_robot._animus_robot_py3',
                             include_dirs=['lib_robot'],
                             libraries=['animus_robot'],
                             library_dirs=['lib_robot'],
                             sources=['lib_robot/animus_robot_py3_wrap.c'],
                             define_macros=[("SWIG", None)],
                             swig_opts=[],
                             extra_link_args=extra_link_args,
                             )

setup(
    name='animus_robot',
    version='3.1.1',
    python_requires='>=3.7',
    description='Animus Robot SDK for Python 3 developed by Cyberselves Universal Ltd.',
    long_description="Animus Robot SDK for Python 3 developed by Cyberselves Universal Ltd.",
    author='Daniel Camilleri',
    author_email='daniel@cyberselves.com',
    url='https://www.cyberselves.com',
    license="Proprietary. (C) Cyberselves Universal Ltd.",
    packages=['animus_robot', 'animus_utils', 'lib_robot'],
    py_modules=['animus_robot', 'animus_utils', 'lib_robot'],
    ext_modules=[animus_robot_py3],
    data_files=[('', ['requirements.txt'])],
    package_data=package_data,
    include_package_data=True,
    install_requires=[
        "numpy >= 1.16.6",
        "opencv-python >= 4.2.0.32",
        "wheel",
        "protobuf ~= 3.15"
    ],
    tests_require=[
        'pytest',
        "protobuf ~= 3.15",
    ],
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Private :: Do not Upload"
        'License :: Other/Proprietary License'
    ],
)
