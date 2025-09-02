# Problemática:
En la actualidad, el dinero se mueve en su mayoría por medios electrónicos, haciendo imperativo que las instituciones bancarias velen por la seguridad en los mivimientos de sus clientes. Sin embargo, por múltiples motivos hackers o demás personas con motivos inescrupulosos, pueden llegar a realizar transacciones desde las cuentas de clientes para robar su dinero. Dado que esto ocurre en segundos, es imperativo que las insituciones bancarias puedan monitorear en tiempo real las transacciones e impedir que las fraudulentas sean completadas.


# Objetivo
Diseñar y desplegar un programa que, haciendo uso de aprendizaje automático de máquina, sea capaz de detectar transacciones fraudulentas en tiempo real.
 

# Metodología

## Elección de dataset y simulación de streaming
Se va a tomar el siguiente dataset (https://www.kaggle.com/datasets/vardhansiramdasu/fraudulent-transactions-prediction) que cuenta con la siguiente información sobre transacciones: step, type, amount, nameOrig, oldbalanceOrg, newbalanceOrig, nameDest, oldbalanceDest, newbalanceDest, isFraud e isFlaggedFraud. Dado que se quiere simular un proceso de streaming, se van a limpiar los datos y haciendo uso de la librería socket se va a enviar la información en tiempo real desde un servidor para que vaya siendo procesada.

## Preprocesamiento

 En primer lugar, se identifica que el dataset tiene columnas que deben ser eliminadas como step (medida de tiempo que no nos interesa), nameOrig, nameDest (dado que no vamos a tener en cuenta el tiempo y hay un número tan grande de valores únicos, no las consideramos relevantes) e isFlaggedFraud (es la predicción de un modelo entonces no nos interesa está variable). A continuación, se identifica que la variable type es importante, pero dado que es categórica debe ser codificada y por tanto se le asigna a cada categoría un valor. Finalmente, se evidencia que el dataset está desbalanceado (hay pocas transacciones fraudulentas en comparación con las no fraudulentas) lo cual puede comprometer el entrenamiento pero en la realidad es bastante probable encontrar datasets de este estilo. 

## Predicción

Como se quiere predecir una variable binaria (es fraudulenta o no es fraudulenta), se va a utilizar un modelo de regresión logística. Además, se va a particionar el dataset 2/3 (entrenamiento y validación) y 1/3 (testeo). El conjunto de entrenamiento y validación va a estar en batch y, por tanto, el modelo de MLib se va a hacer en batch. De hecho, esta información se va a procesar de forma distribuida, donde se van a tener 2 nodos. Se seleccionan tres nodos, dado que el tamaño de los datos (493.53 MB) da para que se puedan hacer particiones (cada una de 120 MB por defecto). De igual manera, el conjunto de testeo va a ser transmitido en streaming y las predicciones sobre la transacción van a ser impresas en consola. Para ello, se va a adaptar el servidor para el envío de los datos. 

## Resultados

Se obtiene un F1-score elevado, lo cual es buano dado el set desbalanceado con el que contamos. Adicionalmente, el proceso de streaming fue exitoso, lo cual permitió simular con bastante precisión lo que ocurre en la realidad. El modelo de regresión logística fue suficiente, pero se podrían explorar otros modelos de clasificación más eficientes y precisos. 

