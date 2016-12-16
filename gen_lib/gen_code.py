# coding=utf-8
from config.type_map import type_map
from config.type_map import type_map_sample
import get_table_info as table_info
from config.config_lib import *

imported_type = ["Integer", "Long", "String"]

FOUR_SPACE = "    "

namespace = get_namespace()
table_field_list, pri_key_info = table_info.get_table_info()
table_name = gen_config['table']
domain_object_alias = get_domain_object_alias_name()
domain_object_name = get_domain_object_name()
data_access_object_name = get_data_access_object_name()
data_access_object_name_impl = get_data_access_object_impl_name()


def gen_xml():
    from lxml import etree
    doc_type = '<!DOCTYPE sqlMap PUBLIC' \
               ' "-//ibatis.apache.org//DTD SQL Map 2.0//EN"' \
               ' "http://ibatis.apache.org/dtd/sql-map-2.dtd">'

    result_map_id = get_java_like_string(table_name) + "ResultMap"

    def get_sql_map():
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
        for field_info in table_field_list:
            column_name = field_info.field_name
            jdbc_type = field_info.field_type
            property_name = get_java_like_string(column_name)
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
        for field_info in table_field_list:
            columns.append("`%s`" % field_info.field_name)

        node.text = ", ".join(columns)
        return node

    def get_select_by_pri_key():

        node = etree.Element("select")
        node.set("id", 'selectByPriKey')
        node.set("parameterClass", type_map[pri_key_info.field_type])
        node.set("resultMap", result_map_id)
        node.text = '\n    SELECT \n    '
        include_node = etree.Element("include", refid="all_column_list")
        node.append(include_node)
        include_node.tail = "\n    FROM %s WHERE %s = #%s#\n  " \
                            % (table_name, pri_key_info.field_name, get_java_like_string(pri_key_info.field_name))
        return node

    def get_insert():
        node = etree.Element("insert")
        node.set("id", "insert")
        node.set("parameterClass", domain_object_alias)
        node.text = "\n    INSERT INTO %s\n    " % table_name
        dynamic_node_declare = etree.Element("dynamic", prepend="(")
        dynamic_node_declare.text = "\n        "
        is_not_null_node = etree.Element("isNotNull")
        is_not_null_node.set("property", get_java_like_string(table_field_list[0].field_name))
        is_not_null_node.text = "`%s`" % table_field_list[0].field_name
        is_not_null_node.tail = "\n        "
        dynamic_node_declare.append(is_not_null_node)

        for field in table_field_list[1:]:
            is_not_null_node = etree.Element("isNotNull")
            is_not_null_node.set("prepend", ",")
            is_not_null_node.set("property", get_java_like_string(field.field_name))
            is_not_null_node.text = "`%s`" % field.field_name
            is_not_null_node.tail = "\n        "
            dynamic_node_declare.append(is_not_null_node)

        is_not_null_node.tail = "\n    )\n    "
        node.append(dynamic_node_declare)
        dynamic_node_declare.tail = "\n    VALUES\n    "

        dynamic_node_value = etree.Element("dynamic", prepend="(")
        dynamic_node_value.text = "\n        "
        is_not_null_node = etree.Element("isNotNull")
        property_str = get_java_like_string(table_field_list[0].field_name)
        is_not_null_node.set("property", property_str)
        is_not_null_node.text = "#%s#" % property_str
        is_not_null_node.tail = "\n        "
        dynamic_node_value.append(is_not_null_node)
        for field in table_field_list[1:]:
            property_str = get_java_like_string(field.field_name)
            is_not_null_node = etree.Element("isNotNull")
            is_not_null_node.set("prepend", ",")
            is_not_null_node.set("property", property_str)
            is_not_null_node.text = "#%s#" % property_str
            is_not_null_node.tail = "\n        "
            dynamic_node_value.append(is_not_null_node)
        is_not_null_node.tail = "\n    )\n    "
        dynamic_node_value.tail = "\n  "
        node.append(dynamic_node_value)
        select_key_node = etree.Element("selectKey")
        select_key_node.set("resultClass", type_map[pri_key_info.field_type])
        select_key_node.set("keyProperty", pri_key_info.field_name)
        select_key_node.text = "SELECT @@IDENTITY AS ID"
        node.append(select_key_node)
        return node

    sql_map.append(get_type_alias())
    sql_map.append(get_result_map())
    sql_map.append(get_all_column_list())
    sql_map.append(get_select_by_pri_key())
    sql_map.append(get_insert())

    return etree.tostring(sql_map, pretty_print=True,
                          xml_declaration=True, encoding='UTF-8',
                          doctype=doc_type)


def gen_domain_object():
    package_str = "package %s;" % gen_config['domain_object_package']
    import_str = []
    field_str = []

    for field in table_field_list:
        var_type = type_map_sample[field.field_type]
        var_class = type_map[field.field_type]
        if var_type not in imported_type:
            imported_type.append(var_type)
            import_str.append("import %s;" % var_class)

        var_name = get_java_like_string(field.field_name)
        func_suffix = "%s%s" % (var_name[0].upper(), var_name[1:])
        declare_str = ""
        if gen_config['is_use_comment'] and field.comment is not None and field.comment != '':
            declare_str = "    /**\n" \
                          "     *%s\n" \
                          "     **/\n" % field.comment

        declare_str = "%s    %s %s;" % (declare_str, var_type, var_name)
        set_fun_str = "    public void set%s(%s %s){\n        this.%s=%s;\n    }" % \
                      (func_suffix, var_type, var_name, var_name, var_name)
        get_fun_str = "    public %s get%s(){\n        return this.%s;\n    }" % \
                      (var_type, func_suffix, var_name)
        field_str.append("%s\n%s\n%s" % (declare_str, set_fun_str, get_fun_str))

    import_str.append("import java.io.Serializable;")
    import_del = "\n".join(import_str)
    main_str = "\n".join(field_str)
    class_str = "%s\n\n%s\n\npublic class %s implements Serializable {\n%s\n}" \
                % (package_str, import_del, domain_object_name, main_str)
    return class_str


def gen_data_access_interface():
    package_str = "package %s;" % gen_config['data_access_package']
    import_declare = ['import %s.%s;' % (gen_config['domain_object_package'], domain_object_name)]
    func_declare = []

    # 生成 select by pri
    var_type = type_map_sample[pri_key_info.field_type]
    if var_type not in imported_type:
        import_declare.append('import %s;' % type_map[pri_key_info.field_type])
    select_pri = "    %s selectByPriKey(%s %s);" % (domain_object_name, var_type,
                                                    get_java_like_string(pri_key_info.field_name))
    func_declare.append(select_pri)

    # 生成 insert
    insert_fun = "    %s insert(%s param);" % (var_type, domain_object_name)
    func_declare.append(insert_fun)

    import_str = '\n'.join(import_declare)
    func_str = '\n'.join(func_declare)

    main_str = "%s\n\n%s\n\npublic interface %s {\n%s\n}" % \
               (package_str, import_str, data_access_object_name, func_str)
    return main_str


def gen_data_access_interface_impl():
    package_str = "package %s;" % gen_config['data_access_impl_package']
    import_declare = ['import %s.%s;' % (gen_config['domain_object_package'], domain_object_name),
                      'import org.springframework.orm.ibatis.support.SqlMapClientDaoSupport;',
                      'import %s.%s;' % (gen_config['data_access_package'], data_access_object_name)]
    func_declare = []

    # 生成 select by pri
    var_type = type_map_sample[pri_key_info.field_type]
    if var_type not in imported_type:
        import_declare.append('import %s;' % type_map[pri_key_info.field_type])

    pri_key_name = get_java_like_string(pri_key_info.field_name)
    select_pri = "%s@Override\n%spublic %s selectByPriKey(%s %s){\n%sreturn (%s)getSqlMapClientTemplate().queryForObject(\"%s.selectByPriKey\", %s);\n%s}" \
                 % (FOUR_SPACE, FOUR_SPACE, domain_object_name, var_type, pri_key_name,
                    FOUR_SPACE * 2, domain_object_name, namespace, pri_key_name,
                    FOUR_SPACE)
    func_declare.append(select_pri)

    # 生成 insert
    insert_fun = "%s@Override\n%spublic %s insert(%s param){\n%sObject result = getSqlMapClientTemplate().insert(\"%s.insert\", param);\n%sif(result==null)result=-1;\n%sreturn (%s)result;\n%s}" \
                 % (FOUR_SPACE, FOUR_SPACE, var_type, domain_object_name, FOUR_SPACE * 2, namespace, FOUR_SPACE * 2, FOUR_SPACE * 2, var_type, FOUR_SPACE)
    func_declare.append(insert_fun)

    import_str = '\n\n'.join(import_declare)
    func_str = '\n\n'.join(func_declare)

    main_str = "%s\n\n%s\n\npublic class %s extends SqlMapClientDaoSupport implements %s {\n%s\n}" % \
               (package_str, import_str, data_access_object_name_impl, data_access_object_name, func_str)
    return main_str


