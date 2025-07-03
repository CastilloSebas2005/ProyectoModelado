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

#### Linux

También puede instalar las mismas manualmente:

``` bash

sudo apt install python3-simpy3
sudo apt install python3-numpy
sudo apt install python3-scipy

```

#### Windows

``` bash
pip3 install -r source/requirements.txt

```

o intalar manualmente uno por uno:

``` bash

pip3 install simpy (a veces este falla y se debe usar simpy3)
pip3 install numpy
pip3 install scipy

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

Para una ejecución más personalizada indicando las duraciones y repeticiones 

``` bash

make runCustom DURATION=10000 SLOW=false RUNS=1 MONITOR=true INTERVAL=1

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

#### Nota

También puede usar un IDE como vscode y presionar el botón

