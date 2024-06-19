# BPPY (Basic Package PYthon)

This Package offer mostly basic Python Functions like encrypting with sha256, using dates and other. The main reason to use this package is the sql.py, because it offers a simple to use sql class to 

### How to use the sql.py

- First you have to create a SQL_CLASS object, and select its sql database type, currently only Mysql and sqlite is supported, just type 'mysql' or 'sqlite'.
- Then you have to use .login() with the parameters. The 'tables' parameter is a list of the tablenames as Stings. You dont have to fill it out, you can also just fill it out in basic_read(), basic_write() or basic_delete(). Just remember you the have to use None to use the original tables.
- The you can then use the basic_read() or basic_write() function or just the Execute_SQL_Command() to use plain text sql querys. The args represent the columns to use and the kwargs are used for a where statement.