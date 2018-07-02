import configparser
import sys
import pur
import os
from ._folder import TmpDir


def _standardize_requirements(req):
    req = req.strip()
    req = req.replace(";", "\n").strip()
    r = req.replace("\n\n", "\n")
    while len(r) < len(req):
        req = r
        r = req.replace("\n\n", "\n")
    req = [r.strip() for r in req.split("\n")]
    return "\n".join(req)


def update_requirements(req):
    req = _standardize_requirements(req)
    with TmpDir() as folder:
        input_file = os.path.join(folder, "requirements.txt")
        output_file = os.path.join(folder, "requirements-output.txt")
        with open(input_file, "w") as f:
            f.write(req)
        pur.update_requirements(input_file=input_file, output_file=output_file)
        with open(output_file, "r") as f:
            data_output = f.read().strip()

        data_input = req.split("\n")
        data_output = data_output.split("\n")
        data = dict(zip(data_input, data_output))

    return data


sections = ["install_requires", "setup_requires", "tests_require"]

config = configparser.ConfigParser()
config.read("setup.cfg")

if "options" not in config.sections():
    sys.exit(0)

req_map = dict()

for s in sections:
    if s in config["options"]:
        req_map[s] = update_requirements(config["options"][s])


def update_setupcfg(filepath, req_map, sections):
    setupcfg = []
    state = "unknown"
    with open(filepath, "r") as f:
        for line in f:
            for s in sections:
                if s in line:
                    state = s
                    break
            else:
                if state in sections:
                    s = line.strip()
                    if state in req_map and s in req_map[state]:
                        line = line.replace(s, req_map[state][s])
            setupcfg.append(line)
    with open(filepath, "w") as f:
        f.write("".join(setupcfg))


update_setupcfg("setup.cfg", req_map, sections)


# def parse_requirements(req):
#     pass


# config.sections()
# config['options']['setup_requires']
# config['options']['install_requires']
# '\nbrent-search>=1.0.31\nndarray-listener>=1.1.0\nnumpy>=1.14.0\npandas>=0.22\npytest>=3.2.5\nscipy>=1.0.0\ntqdm>=4.19.5'

# update_requirements(
#     input_file=options['requirement'],
#     output_file=options['output'],
#     force=options['force'],
#     interactive=options['interactive'],
#     skip=options['skip'],
#     only=options['only'],
#     dry_run=options['dry_run'],
#     no_recursive=options['no_recursive'],
#     echo=options['echo'],
# )

