def do_task():
    with open("schedule_in.xml") as f:
        inp_data = f.read().split("\n")

    out = open("schedule_out.csv", "w")
    out.write("day;lesson_name;start_lesson;end_lesson;teacher;class_number;lesson_type;building\n")

    tags_count = 0
    previous_tags = []
    line_to_add = []
    for s in inp_data:
        current_str = s.replace("  ", "")

        if current_str == "":
            continue

        current_tag = current_str[1:current_str.index(">")]
        if "/" + current_tag in current_str:
            data = current_str[current_str.index(">") + 1:current_str.index("</")]
            line_to_add.append(data)
        else:
            if "/" in current_str:
                if line_to_add:
                    out.write(";".join(previous_tags) + ";" + ";".join(line_to_add))
                    out.write("\n")
                    line_to_add.clear()
                tags_count -= 1
                if previous_tags:
                    previous_tags.pop(-1)
            else:
                tags_count += 1
                if tags_count > 1:
                    previous_tags.append(current_tag)

    out.close()


do_task()
