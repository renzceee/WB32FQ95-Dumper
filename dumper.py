import subprocess
import time
import os
import sys

DFU_CLI = "wb32-dfu-updater_cli.exe"
DUMP_SIZE = 0x40000  # 256 KB
DFU_POLL_INTERVAL = 1  # seconds

def dfu_device_connected():
    try:
        result = subprocess.run([DFU_CLI, "-l"], capture_output=True, text=True)
        return "Found DFU" in result.stdout or "WestBerry" in result.stdout or "[0]" in result.stdout
    except FileNotFoundError:
        print("DFU CLI tool not found. Make sure it's in the same directory.")
        exit(1)

def dump_firmware(output_file):
    print(f"Dumping full 256KB flash to '{output_file}'...")
    result = subprocess.run([
        DFU_CLI, "-t",
        "-s", "0x08000000",
        "-Z", str(DUMP_SIZE),
        "-U", output_file
    ], text=True)
    if result.returncode != 0:
        print("Dump failed!")
        exit(1)
    else:
        print("Dump complete.")

def trim_firmware(input_path, output_path):
    with open(input_path, "rb") as f:
        data = f.read()

    original_size = len(data)
    end = original_size
    while end > 0 and data[end - 1] in (0xFF, 0x00):
        end -= 1

    with open(output_path, "wb") as f:
        f.write(data[:end])

    print(f"Trimmed firmware written to: {output_path}")
    print(f"Original size : {original_size} bytes (0x{original_size:X})")
    print(f"Trimmed size  : {end} bytes (0x{end:X})")

def main():
    if len(sys.argv) != 2:
        print("Usage: app.py <base_name_without_extension>")
        sys.exit(1)

    base_input = sys.argv[1]
    if base_input.lower().endswith(".bin"):
        base_name = base_input[:-4]
    else:
        base_name = base_input

    raw_file = f"{base_name}_raw.bin"
    trimmed_file = f"{base_name}.bin"

    print("Waiting for DFU device to appear...")
    while not dfu_device_connected():
        time.sleep(DFU_POLL_INTERVAL)

    print("DFU device detected.")
    dump_firmware(raw_file)
    trim_firmware(raw_file, trimmed_file)
    print()
    print(f'You can now flash the trimmed firmware:')
    print(f'"{DFU_CLI} -t -D {trimmed_file}"')
    print("All done.")

if __name__ == "__main__":
    main()
