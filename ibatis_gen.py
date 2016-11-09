# coding=utf-8
import gen_lib.get_table_info as table_info
import gen_lib.gen_code as gen_code
from config.sql_config import gen_config
import os

table_field_list = table_info.get_table_info()
pri_key_info = None
for field in table_field_list:
    if field.is_pri_key:
        pri_key_info = field

xml = gen_code.gen_xml(table_field_list)
domain_object = gen_code.gen_domain_object(table_field_list)
access_interface = gen_code.gen_data_access_interface(pri_key_info)
access_interface_impl = gen_code.gen_data_access_interface_impl(pri_key_info)


def get_stand_path(path):
    if path[-1] != "/":
        return path+"/"
    return path


def write_to_file(path, file_name, content):
    path = get_stand_path(path)
    if not os.path.exists(path):
        os.makedirs(path)

    file_path = "%s/%s" % (path, file_name)

    file_fd = open(file_path, "w")
    file_fd.write(content)
    file_fd.close()


class_path = get_stand_path(gen_config['product_path'])

# 生成xml
sql_map_path = get_stand_path(gen_config['sql_map_path'])

xml_path = class_path + sql_map_path
write_to_file(xml_path, "sqlmap_%s.xml" % gen_config['table'], xml)

java_path = get_stand_path(gen_config['java_path'])

# 生成领域对象
domain_object_path = class_path + java_path \
                     + gen_config['domain_object_package'].replace(".", "/")

write_to_file(domain_object_path, "%s.java" % gen_code.get_domain_object_name(), domain_object)

# 生成DAO对象
access_object_path = class_path + java_path \
                     + gen_config['data_access_package'].replace(".", "/")

write_to_file(access_object_path, "%s.java" % gen_code.get_data_access_object_name(), access_interface)

access_impl_object_path = class_path + java_path\
                            + gen_config['data_access_impl_package'].replace(".", "/")
write_to_file(access_object_path, "%s.java" % gen_code.get_data_access_object_impl_name(), access_interface_impl)
exit(0)
