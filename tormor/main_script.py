import click
from tormor.dsn import makeDSN
from tormor.commands import enable_modules, migrate, execute_sql_file, include
from tormor.connections import Connection
import csv

# String of help texts
HELPTEXT = """Tormor -- Migration management

    tormor [opts] command [args]

opts are one or more of:

    -?                      Print this text
    -h hostname             Postgres host
    -d database             Database name
    -u username             Database username (role)
    -p port                 Database port
    -P password             Database password (Not recommended, use environment variable PGPASSWORD instead)

Command is one of:
    enable-modules mod1 [mod2 [mod3 ...]]
        Enable the modules.

    help
        Show this text

    include filename
        Find commands (one per line) in the specified file and run them

    migrate
        Run all migrations.

    sql filename
        Load the filename and present the SQL in it to the database for
        execution. This is useful for choosing migrations scripts to run.

"""

@click.group()
@click.option('-h', nargs=1, required=False, help="Postgres host")
@click.option('-d', nargs=1, required=False, help="Database name")
@click.option('-u', '-U', nargs=1, required=False, help="Database username (role)")
@click.option('-p', nargs=1, required=False, help="Database port")
@click.option('-password', '-P', nargs=1, required=False, help="Database password (Not recommended, use environment variable PGPASSWORD instead)")
@click.pass_context
def script(ctx, h, d, u, p, password):
    cnx_destination = {
        '-h': h,
        '-d': d,
        '-U': u,
        '-p': p,
        '-P': password
    }
    dsn = makeDSN(cnx_destination)
    ctx.obj = {'cnx': Connection(dsn)}

script.add_command(migrate)
script.add_command(enable_modules)
script.add_command(execute_sql_file)
script.add_command(include)

# script()