import re

tags_tree = {"/": {"child": {}, "data": [], "is_list": False}}
tags = ["/"]


def restart():
    global tags_tree, tags

    tags_tree = {"/": {"child": {}, "data": [], "is_list": False}}
    tags = ["/"]


def parse_xml(text: str) -> []:
    inp_data = []
    for s in text.split("\n"):
        s = s.replace("  ", "")
        s = s.replace('"', "'")

        if not s:
            continue

        if re.findall(r">(.*)<", s):
            s = re.sub(r">(.*)<", r">\n\1\n<", s).split("\n")
            inp_data.extend(s)
        else:
            inp_data.append(s)
    return inp_data



def add_tag(tag: str, args: list):
    parent= tags_tree["/"]

    for t in range(1, len(tags)):
        parent = parent["child"][tags[t]]

    if tag not in parent["child"]:
        parent["child"][tag] = {"child": {}, "data": [], "is_list": False}
    else:
        parent["child"][tag]["is_list"] = True

    for a in args:
        parent["child"][tag]["data"].append(f"_{a.replace('=', ': ')}")


def add_data(tag: str, value: str):
    try:
        parent = tags_tree["/"]

        for t in range(1, len(tags)):
            parent = parent["child"][tags[t]]
            if tags[t] == tag:
                break
        parent["data"].append(value)
    except KeyError:
        raise KeyError("Parent tag doesn't exist")


def open_tag_handler(tag: str, args: list):
    add_tag(tag, args)
    tags.append(tag)


def close_tag_handler(tag: str):
    last_tag = tags.pop(-1)
    if last_tag != tag:
        raise Exception(f"Invalid file. Tag {tag} close before {last_tag} close")


def write_yaml(out, tag, tag_name="/", depth=-1):
    if tag_name == "/":
        for t in tag["child"].keys():
            write_yaml(out, tag_name=t, tag=tag["child"][t], depth=depth + 1)
        return

    tag_data = tag["data"]
    out.write("  " * depth + tag_name + ":")

    if len(tag_data) == 1:
        out.write(" " + tag_data[0] + "\n")
    elif len(tag_data) > 1 or tag["child"]:
        out.write("\n")
        for d in tag_data:
            out.write("  " * (depth + 1))
            if tag["is_list"]:
                out.write("- ")
            out.write(d + "\n")

        for t in tag["child"].keys():
            write_yaml(out, tag["child"][t], tag_name=t, depth=depth + 1)
    else:
        out.write(f"''\n")


def do_task():
    restart()

    with open("schedule_in.xml") as f:
        inp_data = parse_xml(f.read())

    for current_str in inp_data:
        open_tag_pattern = r"<([\w='\s]*)>"
        close_tag_pattern = r"</(\w*)>"

        if re.fullmatch(open_tag_pattern, current_str):
            current_tag, *args = re.sub(open_tag_pattern, r"\1", current_str).split()
            open_tag_handler(current_tag, args)
        elif re.fullmatch(close_tag_pattern, current_str):
            current_tag = re.sub(close_tag_pattern, r"\1", current_str)
            close_tag_handler(current_tag)
        else:
            add_data(tags[-1], current_str)

    out = open("schedule_out.yml", mode="w")
    write_yaml(out, tags_tree["/"])
    out.close()


do_task()
