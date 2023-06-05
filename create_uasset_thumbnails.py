import tempfile
import binascii
import argparse
from pathlib import Path

from P4 import P4, P4Exception

P4PORT = "ssl:p4.demo.perforce.rocks:1666"
P4USER = "jlindgren"

p4 = P4()
p4.connect()


def get_uassets(depot_path="//..."):
    return p4.run("files", "-e", f"{depot_path}.uasset")


def create_thumbnail(depot_path: str):
    with tempfile.TemporaryDirectory() as temp_dir:
        print(f"{depot_path}", end=" ")
        temp_file = Path(temp_dir) / "temp.uasset"
        p4.run("print", "-q", "-o", f"{temp_file}", depot_path)

        if image_bytes := extract_image_data(temp_file):
            print("Found image data...", end=" ")
            for attr in ["preview", "thumb", "blur"]:
                args = "-fe"
                hex_string = binascii.hexlify(image_bytes)
                if attr == "blur":
                    args = "-f"
                    hex_string = bytes("U4DbZs009u=X7O9a599t=EtQ~U-U01~C0Mxa", "utf-8")

                p4.run(
                    "attribute",
                    f"{args}",
                    "-n",
                    f"{attr}",
                    "-v",
                    hex_string,
                    f"{depot_path}",
                )
            print("Attributes set.")
        else:
            print("No image data found.")


def extract_image_data(filename):
    with open(filename, "rb") as f:
        data = f.read()

    jpg_start = b"\xFF\xD8\xFF"
    jpg_end = b"\xFF\xD9"
    png_start = b"\x89\x50\x4E\x47\x0D\x0A\x1A\x0A"
    png_end = b"\x49\x45\x4E\x44\xAE\x42\x60\x82"

    start = data.find(jpg_start, 0)
    if start >= 0:
        end = data.find(jpg_end, start) + len(
            jpg_end
        )  # add 2 to include the end marker itself
        if end != -1:
            return data[start:end]
    start = data.find(png_start, 0)
    if start >= 0:
        end = data.find(png_end, start) + len(png_end)
        if end != -1:
            return data[start:end]


def main(changelist):
    description = p4.run_describe(changelist)
    for file in description[0]["depotFile"]:
        if file.endswith(".uasset"):
            create_thumbnail(f"{file}@{changelist}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("changelist")

    parsed_args = parser.parse_args()

    main(parsed_args.changelist)
