# Tormor command line tool

The tool can be used to administer the configuration of the Tormor authentication and authorization system. The tool is accessed through the command `tormor`.

    $ tormor -?
    Manage an Tormor database

        tormor [opts] command [args]

    ...


The `enable-modules` and `migrate` commands are used for managing the Tormor installation.


### Run script in another filename

    include filename

Find commands (one per line) in the specified file and run them


### Run a SQL script

    sql filename

Load the filename and present the SQL in it to the database for execution. This is useful for choosing migrations scripts to run.

