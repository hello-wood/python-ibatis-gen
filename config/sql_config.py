# coding=utf-8
# 数据库连接配置
connect_config = {
    "url": "",
    "user": "",
    "password": "",
    "db": ""
}

# 生成配置
gen_config = {
    # 必填
    "table": "xml_gen_table",
    # 必填
    "product_path": "/Users/linjun/Workspaces/java/test/",
    "java_path": "src/main/java/",
    "sql_map_path": "src/main/resources/dal/sqlmap/",
    #默认 [table].xml
    "sql_map_file_name": None,
    # 必填
    "domain_object_package": "com.test.test.dataobject",
    "domain_object_name": None,
    # 必填
    "data_access_package": "com.test.test.dao",
    "data_access_impl_package": "com.test.test.dao.impl",
    "data_access_interface": None,
    "xml_namespace_prefix": None,
    "is_generate_batch_insert": False,
    "is_use_comment": True,
    "charset": 'utf8'
}


