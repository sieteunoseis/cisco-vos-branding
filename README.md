# Cisco CUCM Branding Generator

This script generates branding assets for Cisco UC applications. It allows you to create custom themes with either solid colors or gradients.

## Official Documentation

The branding customization process is documented in the [Cisco Unified Communications Manager Feature Configuration Guide](https://www.cisco.com/c/en/us/td/docs/voice_ip_comm/cucm/admin/12_5_1/featureConfig/cucm_b_feature-configuration-guide-1251/cucm_b_feature-configuration-guide-1251_chapter_0101011.html). This guide provides comprehensive information about:

- Setting up branding
- System requirements
- File specifications
- Installation procedures
- Troubleshooting

This script helps automate the creation of branding assets according to these specifications.

## Prerequisites

- Python 3.x
- Pillow library (`pip install Pillow`)

## Installation

1. Clone this repository
2. Create a virtual environment (recommended):
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

```bash
python script.py --style [gradient|solid] [options]
```

### Options

- `--style`: Required. Choose between 'gradient' or 'solid'
- `--start-color`: Starting color in hex format (default: #FFFFFF)
- `--end-color`: Ending color in hex format (default: #FF0000)
- `--logo-color`: Color for branding_logo.png text. If not specified, uses end-color
- `--glow`: Add glow effect to the text
- `--antialias`: Enable anti-aliasing for text rendering (default: no)

### Text Formatting

The script supports multi-line text using the `\n` character. For example:
```python
"Automate\nBuilders"  # Creates two lines of text
```

When using multi-line text:
- Each line is automatically centered
- Line spacing is proportional to font size
- All text effects (glow, antialiasing) apply to all lines
- Vertical positioning adjusts automatically to center the entire text block

### Examples

Create a gradient theme:
```bash
python script.py --style gradient --start-color "#FFFFFF" --end-color "#FF0000"
```

Create a solid theme with custom logo color:
```bash
python script.py --style solid --end-color "#FF0000" --logo-color "#000000"
```

Add glow effect:
```bash
python script.py --style gradient --end-color "#FF0000" --glow
```

Enable anti-aliasing for smoother text:
```bash
python script.py --style gradient --end-color "#FF0000" --antialias
```

## Generated Files

The script creates the following directory structure:
```
branding/
├── BrandingProperties.properties
├── branding_logo.png
└── ccmadmin/
    ├── BrandingProperties.properties
    ├── brandingHeaderBegLTR.gif
    ├── brandingHeaderBegRTL.gif
    ├── brandingHeaderEndLTR.gif
    ├── brandingHeaderEndRTL.gif
    ├── brandingHeaderMidLTR.gif
    ├── brandingHeaderMidRTL.gif
    └── ciscoLogo12pxMargin.gif
```

## Reference Images

### Branding-1.png
This image shows the primary UI elements that will be modified:
![Branding 1](/images/branding-1.png)

### Branding-2.png
This image shows the secondary UI elements that will be modified:
![Branding 2](/images/branding-2.png)

## Font Credits

This project uses fonts created by Daniel Linssen:
- [M3x3](https://managore.itch.io/m3x7)
- [M5x7](https://managore.itch.io/m5x7)
- [M6x11](https://managore.itch.io/m6x11)

Please visit the links above to support the font creator and learn more about their work.

## License

MIT License. Please refer to the included LICENSE file for terms of use.

## Contributing

Contributions are welcome. Please fork the repository and submit a pull request with your changes.