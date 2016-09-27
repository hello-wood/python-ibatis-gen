# coding=utf-8
# 数据库连接配置
connect_config = {
    "url": "127.0.0.1",
    "user": "root",
    "password": "52Xlm,./",
    "db": "linjun_db"
}

# 生成配置
gen_config = {
    # 必填
    "table": "xml_gen_table",
    # 必填
    "product_path": "/Users/linjun/Workspaces/java/xman/xman3-new/",
    "java_path": "src/main/java/",
    "sql_map_path": "src/main/resources/dal/sqlmap/",
    #默认 [table].xml
    "sql_map_file_name": None,
    # 必填
    "domain_object_package": "com.zhongan.xman.dataobject",
    "domain_object_name": None,
    # 必填
    "data_access_package": "com.zhongan.xman.dao",
    "data_access_interface": None,
    "xml_namespace_prefix": None,
    "is_generate_batch_insert": False,
    "is_use_comment": True,
    "charset": 'utf8'
}


