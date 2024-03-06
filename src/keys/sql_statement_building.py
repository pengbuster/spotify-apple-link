def build_select_string(table: str, /, cols: tuple[str] = None, arguments: tuple[str] = None) -> str:
    """
    Used to build an SQL SELECT statement to retrieve the rows and columns of the specified tables according to the
        arguments cols and arguments
    :param table: Name of the table to be accessed
    :param cols: Which columns of the table to be returned; if '' then all columns will be returned
                    Each element of cols should be the name of a desired column
    :param arguments: Boolean arguments to select particular rows from the table
    :return: String containing the desired SELECT statement
    """
    # Building the correct substring of which columns to select from the table
    # If cols is non empty tuple, build cols as a string with each of the original elements of the tuple as a comma
    #   separated string
    if cols:
        cols = ', '.join(col for col in cols)

    # If no cols were specified, use * to select all columns
    else:
        cols = '*'

    # Start the SELECT statement with the columns to select from the specified table
    select_string = f'SELECT {cols} FROM {table}'

    # If arguments is non empty tuple, build arguments as a string with each of the original arguments of the tuple
    #   as a string with each element separated by ' AND ' and append it to select_string
    if arguments:
        # Append ' WHERE' to the existing select_string
        select_string = ' '.join((select_string, 'WHERE'))

        # Build arguments into string with each element in arguments separated by ' AND '
        arguments = ' AND '.join(argument for argument in arguments)

        # Append arguments string to existing selec_string
        select_string += ' '.join((select_string, arguments))

    return select_string


def build_insert_string(table: str, cols_count: int) -> str:
    """
    Builds an SQL INSERT statement to insert a new row into the specified table
    Returned statement will have '?' as a placeholder for each argument which will be put back in place by passing
        arguments to sqlite3 during statement execution
    :param table: Name of the table to insert values into
    :param cols_count: Number of columns of the row to be inserted into the table
    :return: String containing an INSERT statement with VALUES equalling '?' repeated cols_count times comma separated
    """
    # Begin the statement by specifying which table to insert values into
    insert_string = f'INSERT INTO {table} VALUES ('

    # Creating values as a string of comma separated ?s repeated cols_count times
    values = ', '.join('?' for _ in range(cols_count))

    # Joining existing insert_string, values, and a closing parentheses together
    insert_string = ''.join((insert_string, values, ')'))

    return insert_string


def build_update_string(table: str, row_key: int, arguments: dict) -> str:
    """
    Used to build a SQL UPDATE statement that will update the fields of a row whose id matches that of id to those
        fields specified in arguments
    The statement will use '?' as a placeholder for each argument, which will be put back in place by passing
        arguments to sqlite3 during statement execution
    :param table: Name of the table whose row will be updated
    :param row_key: Key of the row to be updated
    :param arguments: New values for the specified row
    :return: String containing an UPDATE
    """
    """
    Used to build a SQL UPDATE statement that will update the fields of a row whose
        id matches that of id to those fields specified in arguments
    The statement will use '?' as a placeholder for each argument, which will be put back in
        place by passing arguments to sqlite3 during statement execution
    """
    # Begin the statement by specifying the table to update
    update_string = f'UPDATE {table} SET'

    # Converting arguments into a tuple for better parsing
    arguments = tuple(arguments.items())

    # Parsing each argument in arguments to add to update_string after 'SET'
    for i in range(len(arguments)):
        # Get the name of the current dictionary value key into an easy-to-read variable
        key = arguments[i][0]

        # Add the next argument to the update string
        update_string = ' '.join((update_string, f'{key} = :{key}'))

        # If the argument isn't the last element in arguments, add a comma in preparation
        #   for the next argument to be added after it
        if i < (len(arguments) - 1):
            update_string = ''.join((update_string, ','))

    # After all arguments have been added to update_string, add the where clause
    #   that specifies the id of the row to be updated
    update_string = ' '.join((update_string, f'WHERE {table}_id = {row_key}'))

    return update_string
