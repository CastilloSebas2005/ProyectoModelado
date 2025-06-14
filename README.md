# ProyectoModelado

Parte programada del proyecto de Metodos de Modelado y Optimización

## Manual de usuario

### Dependencias

Se encuentran en el archivo [requirements.txt](./source/requirements.txt)

1. Simpy
2. Scipy
3. Numpy

Para instalar estas dependencias puede hacer uso del makefile:

``` bash

make install

```

También puede instalar las mismas manualmente:

``` bash

sudo apt install python3-simpy3
sudo apt install python3-numpy
sudo apt install python3-scipy

```

### Como ejecutar el programa

#### Usando el Makefile

Debe ubicarse en la raiz de este proyecto y escribir el siguiente comando:

Para ejecutar normalmente

``` bash

make run

```

Para ejecutar en modo despacio y visualizar mejor las interacciones

``` bash

make runSlow

```

#### Desde la terminal

Para ejecutar normalmente

``` bash

python3 <rutaAlArchivo>/main.py

```

Para ejecutar en modo despacio y visualizar mejora las interacciones

``` bash

python3 <rutaAlArchivo>/main.py --duration 50 --slow --sleeptime 0.5 --runs 2

```


### 
