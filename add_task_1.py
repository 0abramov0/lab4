import xmltodict
import yaml


def do_task():
    xml_file = open("schedule_in.xml","r")
    xml_str = xml_file.read()
    data = xmltodict.parse(xml_str)

    out = open("schedule_out.yml","w")
    yaml.dump(data, out)
    out.close()


do_task()
