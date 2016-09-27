# coding=utf-8
import StringIO
from config.sql_config import gen_config
from config.type_map import type_map
from config.type_map import type_map_sample


def gen_xml(table_info_list):
    from lxml import etree
    doc_type = '<!DOCTYPE sqlMap PUBLIC' \
               ' "-//ibatis.apache.org//DTD SQL Map 2.0//EN"' \
               ' "http://ibatis.apache.org/dtd/sql-map-2.dtd">'

    table = gen_config['table']
    domain_object_alias = get_domain_object_alias_name()
    domain_object_name = get_domain_object_name()
    result_map_id = __get_java_like_string(table) + "ResultMap"

    def get_sql_map():
        namespace = gen_config['table']
        set_prefix = gen_config['xml_namespace_prefix']
        if set_prefix is None \
                or set_prefix == '':
            pass
        else:
            namespace = "%s.%s" % (set_prefix, namespace)
        node = etree.Element("sqlMap")
        node.set("namespace", namespace)
        return node

    sql_map = get_sql_map()

    def get_type_alias():
        node = etree.Element("typeAlias")
        node.set("alias", domain_object_alias)
        node.set("type", "%s.%s" % (gen_config['domain_object_package'], domain_object_name))
        return node

    def get_result_map():
        node = etree.Element("resultMap")
        node.set("id", result_map_id)
        node.set("class", domain_object_alias)
        for field_info in table_info_list:
            column_name = field_info.field_name
            jdbc_type = field_info.field_type
            property_name = __get_java_like_string(column_name)
            child_node = etree.Element("result")
            child_node.set("column", column_name)
            child_node.set("jdbcType", jdbc_type)
            child_node.set("property", property_name)
            node.append(child_node)
        return node

    def get_all_column_list():
        node = etree.Element("sql")
        node.set("id", "all_column_list")
        columns = []
        for field_info in table_info_list:
            columns.append("`%s`" % field_info.field_name)

        node.text = ", ".join(columns)
        return node

    def get_select_by_pri_key():
        pri_key_field = ""
        for field_info in table_info_list:
            if field_info.is_pri_key:
                pri_key_field = field_info

        node = etree.Element("select")
        node.set("id", 'selectByPriKey')
        node.set("parameterClass", type_map[pri_key_field.field_type])
        node.set("resultMap", result_map_id)
        node.text = '\n    SELECT \n    '
        include_node = etree.Element("include", refid="all_column_list")
        node.append(include_node)
        include_node.tail = "\n    FROM %s WHERE %s = #%s#\n  " \
                    % (table, pri_key_field.field_name, __get_java_like_string(pri_key_field.field_name))
        return node

    sql_map.append(get_type_alias())
    sql_map.append(get_result_map())
    sql_map.append(get_all_column_list())
    sql_map.append(get_select_by_pri_key())

    return etree.tostring(sql_map, pretty_print=True,
                          xml_declaration=True, encoding='UTF-8',
                          doctype=doc_type)


def gen_domain_object(table_info_list):

    package_str = "package %s;" % gen_config['domain_object_package']
    import_str = []
    field_str = []
    imported_type = {"Integer", "Long", "String"}

    for field in table_info_list:
        var_type = type_map_sample[field.field_type]
        var_class = type_map[field.field_type]
        if var_type not in imported_type:
            imported_type.add(var_type)
            import_str.append("import %s;" % var_class)

        var_name = __get_java_like_string(field.field_name)
        func_suffix = "%s%s" % (var_name[0].upper(), var_name[1:])
        declare_str = "    %s %s;" % (var_type, var_name)
        set_fun_str = "    public void set%s(%s %s){\n        this.%s=%s\n    }" % \
                      (func_suffix, var_type, var_name, var_name, var_name)
        get_fun_str = "    public %s get%s(){\n        return this.%s\n    }" % \
                      (var_type, func_suffix, var_name)
        field_str.append("%s\n%s\n%s" % (declare_str, set_fun_str, get_fun_str))

    import_str.append("import java.io.Serializable;")
    import_del = "\n".join(import_str)
    main_str = "\n".join(field_str)
    class_str = "%s\n%s\npublic class %s implements Serializable {\n%s\n}" \
                % (package_str, import_del, get_domain_object_name(), main_str)
    return class_str


def gen_data_access_interface(pri_key_info):
    domain_object_name = get_domain_object_name()
    package_str = "package %s;" % gen_config['data_access_package']
    import_declare = ['import %s.%s;' % (gen_config['domain_object_package'], domain_object_name)]
    func_declare = []

    imported_type = ["Integer", "Long", "String"]

    var_type = type_map_sample[pri_key_info.field_type]
    if var_type not in imported_type:
        import_declare.append('import %s;' % type_map[pri_key_info.field_type])
    select_pri = "    %s selectByPriKey(%s %s);" % (domain_object_name, var_type,
                                                __get_java_like_string(pri_key_info.field_name))
    func_declare.append(select_pri)
    import_str = '\n'.join(import_declare)
    func_str = '\n'.join(func_declare)

    main_str = "%s\n%s\npublic interface %s {\n%s\n}" %\
               (package_str, import_str, get_data_access_object_name(), func_str)
    return main_str


def __get_java_like_string(input_str, with_first_upper=False):
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
    java_like_table = __get_java_like_string(gen_config['table'])
    return "%c%sDO" % (java_like_table[0].lower(), java_like_table[1:])


def get_domain_object_name():
    java_like_table = __get_java_like_string(gen_config['table'])
    return "%c%sDO" % (java_like_table[0].upper(), java_like_table[1:])


def get_data_access_object_name():
    java_like_table = __get_java_like_string(gen_config['table'])
    return "%c%sDAO" % (java_like_table[0].upper(), java_like_table[1:])


