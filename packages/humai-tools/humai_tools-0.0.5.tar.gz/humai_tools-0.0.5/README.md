# Humai internal tools

Internal tools for development in Humai.
1. Cambiar en init.py la version a un numero distinto, y tambien cambiar la version el en setup.py (ambas al mismo numero pero distinto de numeros anteriores)
2. Hacer push a Github
3. Estando en el directorio donde se encuentra setup.py correr:
- python3 setup.py sdist bdist_wheel

- twine upload dist/*

 
- ingresar nombre de usuario y clave:
    humai
    pyecolatam