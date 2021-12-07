import os

from algorithms.a_star import a_star_timeout, a_star_opt_timeout
from algorithms.ida_star import ida_star_timeout
from algorithms.ucs import ucs_timeout

NSOL = 4
INPUT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "inputs")
OUTPUT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "outputs")
TIMEOUT = 1


def write_out(file, to_write):
    with open(file, 'a') as f:
        f.write(to_write)

def get_or_create_folder(path):
    if not os.path.exists(path):
            os.makedirs(path)
    return path

def write_results(result, output_file_path, euristica=None):
    if isinstance(result, tuple):
        if euristica != None:
            write_out(output_file_path,'\n'+ euristica + '\n')
        for index, r in enumerate(result[0]):
            write_out(output_file_path, r)
            write_out(output_file_path, "timp solutie: {}\n".format(result[3][index]))
        write_out(output_file_path, "noduri in memorie: {}\n".format(result[1]))
        write_out(output_file_path, "noduri procesate: {}\n".format(result[2]))
        write_out(output_file_path, "\n")
    else:
        write_out(output_file_path, result)

def run_ucs(file):
    result = ucs_timeout(os.path.join(INPUT_PATH, file), NSOL, timeout=TIMEOUT)
    output_folder = get_or_create_folder(os.path.join(OUTPUT_PATH, "ucs"))
    output_file_path = os.path.join(output_folder, "output_for_"+file)
    with open(output_file_path, 'w') as f:
        f.write("")
    write_results(result, output_file_path)


def run_a_star(file):
    euristici = ["euristica banala", "euristica manhattan", "euristica euclidiana", " euristica neadmisibila"]

    output_folder = get_or_create_folder(os.path.join(OUTPUT_PATH, "a_star"))
    output_file_path = os.path.join(output_folder, "output_for_" + file)
    with open(output_file_path, 'w') as f:
        f.write("")
    for euristica in euristici:
        result = a_star_timeout(os.path.join(INPUT_PATH, file), NSOL, euristica, timeout=TIMEOUT)
        write_results(result, output_file_path, euristica)

def run_a_star_opt(file):
    euristici = ["euristica banala", "euristica manhattan", "euristica euclidiana", "euristica neadmisibila"]

    output_folder = get_or_create_folder(os.path.join(OUTPUT_PATH, "a_star_opt"))
    output_file_path = os.path.join(output_folder, "output_for_" + file)
    with open(output_file_path, 'w') as f:
        f.write("")
    for euristica in euristici:
        result = a_star_opt_timeout(os.path.join(INPUT_PATH, file), euristica, timeout=TIMEOUT)
        write_results(result, output_file_path, euristica)

def run_ida_star(file):
    euristici = ["euristica banala", "euristica manhattan", "euristica euclidiana", "euristica neadmisibila"]

    output_folder = get_or_create_folder(os.path.join(OUTPUT_PATH, "ida_star"))
    output_file_path = os.path.join(output_folder, "output_for_" + file)
    with open(output_file_path, 'w') as f:
        f.write("")
    for euristica in euristici:
        result = ida_star_timeout(os.path.join(INPUT_PATH, file), NSOL, euristica, timeout=TIMEOUT)
        write_results(result, output_file_path, euristica)


for file in os.listdir(INPUT_PATH):
    run_ucs(file)

    run_a_star(file)

    run_a_star_opt(file)

    run_ida_star(file)