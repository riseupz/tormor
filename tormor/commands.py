from tormor.exceptions import SchemaNotPresent
import csv

# String of queries to add module
ADD_MODULE = """INSERT INTO module(name) VALUES($1)"""

# String of queries to create table 'module' and 'migration'
BOOTSTRAP_SQL = """
CREATE TABLE module (
    name text NOT NULL,
    CONSTRAINT module_pk PRIMARY KEY(name)
);

CREATE TABLE migration (
    module_name text NOT NULL,
    CONSTRAINT migration_module_fkey
        FOREIGN KEY (module_name)
        REFERENCES module (name) MATCH SIMPLE
        ON UPDATE NO ACTION ON DELETE NO ACTION DEFERRABLE,
    migration text NOT NULL,
    CONSTRAINT migration_pk PRIMARY KEY (module_name, migration)
);
"""

def migrate(conn, dry_run):
    if not dry_run:
        print("NOT DRY RUN")
    else:
        print("DRY RUN")

def enable_modules(conn, modules):
    modules_to_be_added = set(modules)
    try:
        current_modules = conn.load_modules()
    except SchemaNotPresent:
        print("No existing module table. Bootstrapping...")
        conn.execute(BOOTSTRAP_SQL)
        current_modules = conn.load_modules()
    for each_module in modules_to_be_added.difference(current_modules):
        conn.execute(ADD_MODULE.replace("$1", "\'" + each_module +"\'"))
        print(each_module, "enabled")

def execute_sql_file(conn, filename):
    try:
        with open(filename) as f:
            commands = f.read()
            conn.execute(commands)
        conn.load_modules()
        print(filename, "successfully executed")
    except Exception:
        print("Error whilst running", filename)
        raise

def migrate_sql_file(conn, module, migration, filename):
    return
