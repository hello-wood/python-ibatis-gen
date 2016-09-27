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


def get_stand_path(path):
    if path[-1] != "/":
        return path+"/"
    return path

class_path = get_stand_path(gen_config['product_path'])

# 生成xml
sql_map_path = get_stand_path(gen_config['sql_map_path'])

xml_path = class_path + sql_map_path
if not os.path.exists(xml_path):
    os.makedirs(xml_path)

xml_file = "%ssqlmap_%s.xml" % (xml_path, gen_config['table'])

xml_fd = open(xml_file, "w")
xml_fd.write(xml)
xml_fd.close()

java_path = get_stand_path(gen_config['java_path'])
# 生成领域对象
domain_object_path = class_path + java_path \
                     + gen_config['domain_object_package'].replace(".", "/")

if not os.path.exists(domain_object_path):
    os.makedirs(domain_object_path)

domain_object_file = "%s/%s.java" % (domain_object_path, gen_code.get_domain_object_name())

domain_object_fd = open(domain_object_file, "w")
domain_object_fd.write(domain_object)
domain_object_fd.close()

# 生成DAO对象
access_object_path = class_path + java_path \
                     + gen_config['data_access_package'].replace(".", "/")

if not os.path.exists(access_object_path):
    os.makedirs(access_object_path)

access_object_file = "%s/%s.java" % (access_object_path, gen_code.get_data_access_object_name())

access_object_fd = open(access_object_file, "w")
access_object_fd.write(access_interface)
access_object_fd.close()
exit(0)
