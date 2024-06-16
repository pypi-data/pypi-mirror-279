from setuptools import setup
try:
    import multiprocessing
except ImportError:
    pass

setup(
    name='httpie-digirm-auth',
    description='DigiRM plugin for HTTPie.',
    long_description=open('README.rst').read().strip(),
    version='0.2.0',
    author='Fred A Kulack',
    author_email='kulack@gmail.com',
    license='MIT',
    url='https://github.com/kulack/httpie-digirm-auth',
    download_url='https://github.com/kulack/httpie-digirm-auth',
    py_modules=['httpie_digirm_auth'],
    zip_safe=False,
    entry_points={
        'httpie.plugins.auth.v1': [
            'httpie_digirm_auth = httpie_digirm_auth:DigiRMAuthPlugin'
        ]
    },
    install_requires=[
        'httpie>=3.2.2'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python',
        'Intended Audience :: Developers',
        'Environment :: Plugins',
        'License :: OSI Approved :: MIT License',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Utilities'
    ],
)
