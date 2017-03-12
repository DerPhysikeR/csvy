#!/usr/bin/env python
"""
2016-11-18 22:42:29
@author: Paul Reiter
"""
from io import StringIO
import yaml
from operator import methodcaller


def read_header(lines):
    """Removes first character from each line in `lines` and parses
    them with yaml.

    Parameters
    ----------
    lines : list
        list of strings representing lines in a text file

    Returns
    -------
    dict
        dictionary containing the yaml-parsed data from lines
    """
    return yaml.load(StringIO(''.join([line[1:] for line in lines])))


def comment(lines, comment_char):
    """Adds a `comment_char` to each line in `lines` and joins them
    with `\n`.

    Parameters
    ----------
    lines : list
        list of strings representing lines in a text file
    comment_char : str
        comment character to be added at the beginning of each line

    Returns
    -------
    str
        Concantenated lines with comment_char at the beginning and `\n` at the
        end of each line.
    """
    return '\n'.join([comment_char + line for line in lines])


def yaml_reader(reader, comment_char='#'):
    """Defines a reader function for csv files with yaml header.

    This is a decorator for file reader functions like `pd.read_csv`,
    which enables to read yaml coded data in the commented head of a
    csv file.

    Parameters
    ----------
    reader : function
        function to be used to read file content
    comment_char : str
        beginning character for the lines containing the yaml header

    Returns
    -------
    function
        Function with identical arguments as `reader` but which returns a
        tuple containing (header, content) of the file to be read.
    """
    def read_with_yaml_header(*args, **kwargs):
        with open(args[0], 'r') as stream:
            filecontent = stream.readlines()
        for i, line in enumerate(filecontent):
            if line[0] != comment_char:
                break
        header = read_header(filecontent[:i])
        csvcontent = reader(StringIO(''.join(filecontent[i:])),
                            *args[1:], **kwargs)
        return header, csvcontent
    return read_with_yaml_header


def yaml_writer(writer, comment_char='#'):
    """Defines a writer function for csv files with yaml header.

    This is a decorator for file writer functions like `pd.to_csv`,
    which enables to write yaml coded data in the commented head of a
    csv file.

    Parameters
    ----------
    writer : function
        function to be used to write file content
    comment_char : str
        beginning character for the lines containing the yaml header

    Returns
    -------
    function
        Function with similar arguments as `writer` but with header and
        content to write as the first two arguments.
    """
    def write_with_yaml_header(header, data_object, *args, **kwargs):
        content = StringIO()
        yaml.dump(header, content)
        written_header = comment(content.getvalue().split('\n')[:-1], '#')
        with open(args[0], 'w') as stream:
            stream.writelines(written_header + '\n')
            f = methodcaller(writer, stream, *args[1:], **kwargs)
            f(data_object)
    return write_with_yaml_header
