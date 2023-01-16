# Precios de productos
 Webscraping realizado con BS4 y Selenium para obtener precios historicos de la gran mayoria de los items de Ragnarok Online (los ids rondan entre el 501 y el 22000 aproximadamente, depende del servidor)
 El scrapeo se preocupa de las cartas que tiene cada arma, de cada roll, ademas se preocupa si el arma es un item "etc" o un equipo.

 ## Creacion tabla SQL
 En la carpeta 'sql-scripts' se encuentra el script para crear la tabla y el script para introducir un .csv de manera más rapida sin el import wizzard.

 ## NOTA
 Para poder realizar el LOAD DATA LOCAL INFILE es necesario lo siguiente(copio y pego de stack overflow):

"If you are trying this on MySQL Workbench,

Go to connections -> edit connection -> select advanced tab

and add OPT_LOCAL_INFILE=1 in the 'Others' text field.

Now restart the connection and try."

Fuente : 

https://stackoverflow.com/questions/2221335/access-denied-for-load-data-infile-in-mysql


## Sevidor de Ragnarok y página a scrapear
https://projectalfheim.net/?module=market

Si juegas RO y llegas a leer esto, somos un grupo de 8 amigos leveleando en el unico server decent low rates pre renewal :P.
Nick ingame : Modigliani,Modiglianus

