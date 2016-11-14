# coding=utf-8
import gen_lib.gen_code as gen_code
from config.sql_config import gen_config
import os

confim = raw_input("确认生成？生成会覆盖原来的文件。（y 继续）:")
print confim
if confim.lower() != 'y':
    exit(0)

xml = gen_code.gen_xml()
domain_object = gen_code.gen_domain_object()
access_interface = gen_code.gen_data_access_interface()
access_interface_impl = gen_code.gen_data_access_interface_impl()
print "success!"


def write_to_file(path, file_name, content):
    if not os.path.exists(path):
        os.makedirs(path)

    file_path = os.path.join(path, file_name)

    file_fd = open(file_path, "w")
    file_fd.write(content)
    file_fd.close()

class_path = gen_config['product_path']

xml_path = os.path.join(class_path, gen_config['sql_map_path'])
write_to_file(xml_path, "sqlmap_%s.xml" % gen_config['table'], xml)

java_path = gen_config['java_path']

# 生成领域对象
domain_object_path = os.path.join(class_path, java_path,
                                  gen_config['domain_object_package'].replace(".", "/"))

write_to_file(domain_object_path, "%s.java" % gen_code.domain_object_name, domain_object)

# 生成DAO对象
access_object_path = os.path.join(class_path, java_path,
                                  gen_config['data_access_package'].replace(".", "/"))

write_to_file(access_object_path, "%s.java" % gen_code.data_access_object_name, access_interface)

access_impl_object_path = os.path.join(class_path, java_path,
                                       gen_config['data_access_impl_package'].replace(".", "/"))
write_to_file(access_impl_object_path, "%s.java" % gen_code.data_access_object_name_impl, access_interface_impl)
exit(0)
