# WB32 Firmware Dumper

A simple Python script to safely **dump and trim firmware** from a WB32 (WestBerry WB32FQ95) microcontroller using `wb32-dfu-updater_cli.exe`.

This tool:
- Waits for a DFU-capable WB32 device
- Dumps the full 256KB firmware to a file
- Trims the dump to remove trailing `0xFF` and `0x00` padding
- Outputs a safe, flashable firmware file

---

## 📦 Requirements

- Python 3.x
- `wb32-dfu-updater_cli.exe` (must be in the same directory or in your PATH)
- Compatible microcontroller in DFU mode (e.g. WB32FQ95)

---

## 🚀 Usage

### Run the script:
```bash
python dumper.py <firmware_name>
