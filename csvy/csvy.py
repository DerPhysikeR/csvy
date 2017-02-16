#!/usr/bin/env Python
"""
2016-11-18 22:42:29
@author: Paul Reiter
"""
from io import StringIO
import yaml
from operator import methodcaller


def load_yaml(stream):
    try:
        content = yaml.load(stream)
    except yaml.YAMLError as exc:
        print(exc)
    return content


def read_header(lines):
    return load_yaml(StringIO(''.join([line[1:] for line in lines])))


def comment(lines, comment_char):
    return '\n'.join([comment_char + line for line in lines])


def write_header(path, data):
    with open(path, 'w') as stream:
        yaml.dump(data, stream)


def yaml_reader(reader, comment_char='#'):
    def read_with_header(*args, **kwargs):
        with open(args[0], 'r') as stream:
            filecontent = stream.readlines()
        for i, line in enumerate(filecontent):
            if line[0] != comment_char:
                break
        header = read_header(filecontent[:i])
        csvcontent = reader(StringIO(''.join(filecontent[i:])),
                            *args[1:], **kwargs)
        return header, csvcontent
    return read_with_header


def yaml_writer(writer):

    def write_with_header(header, data_object, *args, **kwargs):
        content = StringIO()
        yaml.dump(header, content)
        written_header = comment(content.getvalue().split('\n')[:-1], '#')
        with open(args[0], 'w') as stream:
            stream.writelines(written_header + '\n')
            f = methodcaller(writer, stream, *args[1:], **kwargs)
            f(data_object)
    return write_with_header
