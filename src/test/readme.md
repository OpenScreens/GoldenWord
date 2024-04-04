# Testing  
Se realizan todos los comando siguientes desde la terminal de wsl

- Se realizan los commits  con el comando git add . y luego git commit -m ".." 
- Si no quiere verificar con el hook precommit usar --no-verify
- Al ejecutar *python3 test/testflask*, se debe realizar la request GET a http://localhost:5000/testinput para dar comienzo al ciclo.