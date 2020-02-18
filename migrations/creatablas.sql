DROP TABLE IF EXISTS tareas;

CREATE TABLE "tareas" (
	"id"	INTEGER PRIMARY KEY AUTOINCREMENT,
	"titulo"	TEXT NOT NULL,
	"descripción"	TEXT,
	"date"	TEXT NOT NULL
)