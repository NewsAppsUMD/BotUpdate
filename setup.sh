pip install datasette sqlite_utils

datasette install datasette-codespaces

rm #(database name here)

sqlite-utils insert #(database name) (title of dataabase) (name of csv file).csv --csv

datasette #(database name here)