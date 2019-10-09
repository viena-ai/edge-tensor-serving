import subprocess

cmd = "saved_model_cli"
arg1 = "show"
arg2 = "--dir"
arg3 = "/home/viena/tf_files/serving_model/1"
arg4 = "--all"


def inspect_models(model_path):
    global arg3
    arg3 = model_path
    proc1 = subprocess.Popen([cmd, arg1, arg2, arg3], stdout=subprocess.PIPE)

    global tag_set
    global method_name
    global input_params
    global output_params

    tag_set = 'serve'
    method_name = ''
    input_params = []
    output_params = []

    while True:
        line = proc1.stdout.readline()
        if not line:
            break

        line_str = line.decode().strip()

        if line_str.endswith('tag-sets:'):
            line2 = proc1.stdout.readline()
            tag_set = line2.decode().strip()

    proc2 = subprocess.Popen([cmd, arg1, arg2, arg3, arg4], stdout=subprocess.PIPE)

    while True:
        line = proc2.stdout.readline()
        if not line:
            break

        line_str = line.decode().strip()

        if line_str.startswith('inputs'):
            for i in range(3):
                line2 = proc2.stdout.readline()
                line2_str = line2.decode().strip()

                line2_str_split = line2_str.split(":", 1)

                type = line2_str_split[0].strip()
                value = line2_str_split[1].strip()

                if type == 'name':
                    input_params.append(value)

                # print (type, value)

        elif line_str.startswith('outputs'):
            for i in range(3):
                line2 = proc2.stdout.readline()
                line2_str = line2.decode().strip()

                line2_str_split = line2_str.split(":", 1)

                type = line2_str_split[0].strip()
                value = line2_str_split[1].strip()

                if type == 'name':
                    output_params.append(value)

        elif line_str.startswith('Method name is'):
            line3_str_split = line_str.split(":", 1)
            method_name = line3_str_split[1].strip()

    return tag_set, method_name, input_params, output_params


if __name__ == '__main__':
    # model_path = "/home/viena/tf_files/model_1/1"
    model_path = "/home/viena/tf_files/model_2/1"
    tag_set, method_name, input_params, output_params = inspect_models(model_path)

    print(model_path)
    print("----")
    print(tag_set)
    print(method_name)
    print(input_params)
    print(output_params)
