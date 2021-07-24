from setuptools import setup, find_packages


setup(
    name = 'nbconvert-example-templates',
    version = '0.1.1',
    description = "A pip installable nbconvert template example.",
    url = "https://github.com/sheeshee/nbconvert-template-example",
    author = "Samuel Sheehy",
    author_email = "samuelsheehy95@gmail.com",
    license = "MIT",
    packages = find_packages(),
    install_requires = [
        'nbconvert>=6.0.7',
        'jupyter'
    ],
    include_package_data=True,
    entry_points = {
        'nbconvert.exporters': [
            'avocado = avocado:AvocadoExporter',
        ]
    }
)
