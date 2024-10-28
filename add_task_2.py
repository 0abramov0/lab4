import re


def do_task():
    with open("schedule_in.xml") as f:
        inp_data = f.read().split("\n")

    out = open("schedule_out.yml", "w")

    tags_count = 0
    pattern = re.compile(r"<(\w+)>(.*)</\1>")
    for s in inp_data:
        current_str = re.sub(r"\s{2,}", r"", s)

        if current_str == "":
            continue

        current_tag = re.search(r"\w+", current_str).group()

        if pattern.fullmatch(current_str):
            data = pattern.sub(r"\2", current_str)
            out.write("  " * tags_count + f'{current_tag}: "{data}"')
            out.write("\n")
        else:
            if re.findall(r"/", current_str):
                tags_count -= 1
            else:
                out.write("  " * tags_count + f"{current_tag}:")
                out.write("\n")
                tags_count += 1

    out.close()


do_task()
