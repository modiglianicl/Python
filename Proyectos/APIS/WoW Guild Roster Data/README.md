# WoW API - Datos de los miembros de cualquier guild en la region OCE y Americas

## WoW-API-guildmembers.py

Programa que se autentifica con OAuth 2.0 al endpoint de los datos de guild y míticas para obtención de datos de todos los miembros de una guild. Es capaz de identificar quien no ha hecho miticas plus y errores 404 en caso de usuarios inactivos.
Obtiene datos como nombre,clase,spec activa, ilvl, rating m+, mejor rating, mejor llave, nivel mejor llave

## guild_roster_wow.csv

Ejemplo de como quedan los datos en un archivo CSV, en este caso la guild es "Silver Sword" del realm "Ragnaros"

## Carpeta error_logs

contiene un .txt en donde dumpea que miembro de la guild no pudo obtener los datos con indice y nombre.

