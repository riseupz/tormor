import click
from tormor.dsn import makeDSN
from tormor.commands import enable_modules, migrate, execute_sql_file
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

def include(conn, files):
    try:
        for each_file in files:
            with open(each_file, newline="") as f:
                lines = csv.reader(f, delimiter=" ")
                for each_line in lines:
                    if len(each_line) and not each_line[0].startswith("#"):
                        cmd = each_line.pop(0)
                        if cmd == "migrate" and each_line[0] == '--dry-run':
                            run_command(conn, cmd, None, True)
                        else:
                            run_command(conn, cmd, [p for p in each_line if p])
    except:
        print("Error whilst running")

# Dictionary of possible commands
COMMANDS = {
    "enable-modules": enable_modules,
    "migrate": migrate,
    "include": include,
    "sql": execute_sql_file,
}

def run_command(cnx, cmd, args, dry_run=False):
    if cmd == "migrate" and not args:
        COMMANDS[cmd](cnx, dry_run)
    elif cmd == "migrate" and args:
        raise click.ClickException("Error in migrate function")
    elif not args:
        raise click.ClickException("Missing parameter for the command")
    else:
        COMMANDS[cmd](cnx, args)

@click.command()
@click.option('-h', nargs=1, required=False)
@click.option('-d', nargs=1, required=False)
@click.option('-u', '-U', nargs=1, required=False)
@click.option('-p', nargs=1, required=False)
@click.option('-password', '-P', nargs=1, required=False)
@click.option('--help', is_flag=True)
@click.argument('command', required=False)
@click.argument('arguments', required=False, nargs=-1)
@click.option('--dry-run', is_flag=True)
def script(h, d, u, p, password, help, command, arguments, dry_run):
    cnx_destination = {
        '-h': h,
        '-d': d,
        '-U': u,
        '-p': p,
        '-P': password
    }
    dsn = makeDSN(cnx_destination)
    cnx = Connection(dsn)
    if help:
        return click.echo(HELPTEXT)
    # elif command == "migrate" and not dry_run:
    #     return click.echo(command)
    # elif command == "migrate" and dry_run:
    #     return click.echo("dry run migrate")
    # elif command == "include" and arguments:
    #     return click.echo(command + str(arguments))
    # elif command == "include" and not arguments:
    #     raise click.ClickException("Missing file to be included")
    # elif command == "enable-modules" and arguments:
    #     return click.echo(command + str(arguments))
    # elif command == "enable-modules" and not arguments:
    #     raise click.ClickException("Missing module name to be enabled")
    # elif command == "sql" and arguments:
    #     return click.echo(command + str(arguments))
    # elif command == "sql" and not arguments:
    #     raise click.ClickException("Missing sql file to be executed")
    elif command in COMMANDS:
        run_command(cnx, command, arguments, dry_run)
    else:
        raise click.ClickException("Unknown command")

# script()