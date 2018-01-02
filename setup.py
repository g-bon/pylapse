from distutils.core import setup


REQUIRES = [
    'asyncio'
]

TEST_REQUIRES = [
    'pytest'
]

setup(
    name='pylapse',
    version='0.1',
    packages=['pylapse'],
    url='https://github.com/g-bon/pylapse',
    license='MIT',
    author='Gabriele Bonetti',
    author_email='gabriele.bonetti@gmail.com',
    description='An automatic timelapse creator from public webcams',
    install_requires=REQUIRES,
    tests_require=TEST_REQUIRES,
    entry_points={
        'console_scripts': [
            "pylapse = pylapse.pylapse:main"
        ]
    },
)
