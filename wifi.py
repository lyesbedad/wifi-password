import subprocess
import argparse
import os


def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--output", type=str, default="./output/save_wifi")
    return parser.parse_args()


args = parse()
os.makedirs(args.output, exist_ok=True)
data = (
    subprocess.check_output(["netsh", "wlan", "show", "networks"])
    .decode("utf-8", errors="backslashreplace")
    .split("\n")
)
profiles = [i.split(":")[1][1:-1] for i in data if "SSID" in i]


for i in profiles:
    with open(f"{args.output}/alpha.txt", "w") as f:
        f.write(str(profiles))
    break
    try:
        results = (
            subprocess.check_output(
                ["netsh", "wlan", "show", "profile", i, "key=clear"]
            )
            .decode("utf-8", errors="backslashreplace")
            .split("\n")
        )
        results = [b.split(":")[1][1:-1] for b in results if "Contenu de la cl" in b]
        try:
            print("{:<30}| {:<}".format(i, results[0]))
        except IndexError:
            print("{:<30}| {:<}".format(i, ""))

    except subprocess.CalledProcessError:
        print("{:<30}| {:<}".format(i, "ENCODING ERROR"))
