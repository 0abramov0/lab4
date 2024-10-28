def do_task():
    with open("schedule_in.xml") as f:
        inp_data = f.read().split("\n")

    out = open("schedule_out.yml", "w")

    tags_count = 0
    for s in inp_data:
        current_str = s.replace("  ", "")
        if current_str == "":
            continue
        current_tag = current_str[1:current_str.index(">")]
        if "/" + current_tag in current_str:
            data = current_str[current_str.index(">") + 1:current_str.index("</")]
            out.write("  " * tags_count + f'{current_tag}: "{data}"')
            out.write("\n")
        else:
            if "/" in current_str:
                tags_count -= 1
            else:
                out.write("  " * tags_count + f"{current_tag}:")
                out.write("\n")
                tags_count += 1

    out.close()


do_task()
