import os

from tormor.connection import SchemaNotPresent, execute_migration

MYDIR = os.path.dirname(os.path.abspath(__file__))

ADD_MODULE = """INSERT INTO module VALUES (%s)"""

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


class SchemaFilesNotFound(Exception):
    pass


def _get_schema_files_path():
    env_schema_path = os.getenv("SCHEMA_PATH")
    if env_schema_path:
        return env_schema_path.split(os.pathsep)
    return [os.path.join(MYDIR, "../../Schema")]


DEFAULT_SCHEMA_FILES_PATH = _get_schema_files_path()


def find_schema_paths(schema_files_path=DEFAULT_SCHEMA_FILES_PATH):
    """Searches the locations in the `SCHEMA_FILES_PATH` to
    try to find where the schema SQL files are located.
    """
    paths = []
    for path in schema_files_path:
        if os.path.isdir(path):
            paths.append(path)
    if paths:
        return paths
    raise SchemaFilesNotFound("Searched " + os.pathsep.join(schema_files_path))


def enablemodules(cnx, *modules):
    want = set(modules)
    try:
        got = cnx.load_modules()
    except SchemaNotPresent:
        cnx.pg.rollback()
        print("Tormor not loaded for this database. Bootstrapping...")
        cnx.execute(BOOTSTRAP_SQL)
        got = cnx.load_modules()
    for mod in want.difference(got):
        cnx.execute(ADD_MODULE, (mod,))
        print(mod, "enabled")
    cnx._modules = set()


def migrate(cnx):
    ## Find and execute all migration scripts that haven't already been run
    paths = find_schema_paths()
    migrations = set(cnx.select("SELECT module_name, migration FROM migration"))

    for path in paths:
        scripts = []
        for dirname, subdirs, files in os.walk(path):
            relpath = os.path.relpath(dirname, path)
            if relpath != "." and relpath in cnx.load_modules():
                scripts += [(relpath, f) for f in files if f.endswith(".sql")]

        scripts.sort(key=lambda m: m[1])

        for (mod, migration) in scripts:
            if (mod, migration) not in migrations:
                execute_migration(cnx, mod, migration, os.path.join(path, mod, migration))
