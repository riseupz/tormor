from tormor.exceptions import SchemaNotPresent
import csv
import click

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
@click.group()
def subcommand():
    pass

@subcommand.command('migrate')
@click.pass_context
@click.option('--dry-run', is_flag=True)
def migrate(ctx, dry_run):
    """Run all migrations"""

    conn = ctx.obj['cnx']
    if not dry_run:
        print("NOT DRY RUN")
    else:
        print("DRY RUN")

@subcommand.command('enable-modules')
@click.pass_context
@click.argument('modules', required=True, nargs=-1)
def enable_modules(ctx, modules):
    """Enable modules"""

    conn = ctx.obj['cnx']
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

@subcommand.command('sql')
@click.pass_context
@click.argument('sqlfile', nargs=1)
def execute_sql_file(ctx, sqlfile):
    """
    Execute SQL queries in files, useful for running migration scripts
    """

    try:
        conn = ctx.obj['cnx']
        with open(sqlfile) as f:
            commands = f.read()
            conn.execute(commands)
        conn.load_modules()
        print(sqlfile, "successfully executed")
    except Exception:
        print("Error whilst running", sqlfile)
        raise

@subcommand.command()
@click.pass_context
@click.argument('filename', required=True, nargs=1)
def include(ctx, filename):
    """Run all commands inside a file"""
    try:
        with open(filename, newline="") as f:
            lines = csv.reader(f, delimiter=" ")
            for each_line in lines:
                if len(each_line) and not each_line[0].startswith("#"):
                    cmd = each_line.pop(0)
                    print(cmd)
                    if cmd == "migrate":
                        if len(each_line) == 0:
                            ctx.invoke(migrate, dry_run = False)
                        elif len(each_line) == 1:
                            ctx.invoke(migrate, dry_run = True if each_line[0] == '--dry-run' else False)
                        else:
                            raise click.ClickException("Error in migrate command")
                    elif cmd == "enable-modules":
                        ctx.invoke(enable_modules, modules = each_line)
                    elif cmd == "sql" and len(each_line) == 1:
                        ctx.invoke(execute_sql_file, sqlfile = each_line[0])
                    else:
                        raise click.ClickException("Unknown command or parameter")
    except:
        print("Error whilst running")

def migrate_sql_file(conn, module, migration, filename):
    return
