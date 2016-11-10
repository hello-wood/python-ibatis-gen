# coding=utf-8
import StringIO

from sql_config import *


def get_java_like_string(input_str, with_first_upper=False):
    """
    获得java格式的字符串
    """
    string_buf = StringIO.StringIO()
    change_up = False
    for char in input_str:
        if change_up:
            string_buf.write(char.upper())
            change_up = False
            continue
        if char == '_':
            change_up = True
            continue
        string_buf.write(char)
    output_str = string_buf.getvalue()
    string_buf.close()
    if with_first_upper:
        return "%s%s" % (output_str[0].upper(), output_str[1:])
    return output_str


def get_domain_object_alias_name():
    """
    获得领域对象别名
    """
    java_like_table = get_java_like_string(gen_config['table'])
    return "%c%sDO" % (java_like_table[0].lower(), java_like_table[1:])


def get_domain_object_name():
    java_like_table = get_java_like_string(gen_config['table'])
    return "%c%sDO" % (java_like_table[0].upper(), java_like_table[1:])


def get_data_access_object_name():
    java_like_table = get_java_like_string(gen_config['table'])
    return "%c%sDAO" % (java_like_table[0].upper(), java_like_table[1:])


def get_data_access_object_impl_name():
    java_like_table = get_java_like_string(gen_config['table'])
    return "%c%sDAOImpl" % (java_like_table[0].upper(), java_like_table[1:])


def get_namespace():
    gen_namespace = gen_config['table']
    set_prefix = gen_config['xml_namespace_prefix']
    if set_prefix is None \
            or set_prefix == '':
        pass
    else:
        gen_namespace = "%s.%s" % (set_prefix, gen_namespace)
    return gen_namespace
