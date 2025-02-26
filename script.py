#!/usr/bin/env python
from PIL import Image, ImageDraw, ImageFont
import os
import argparse
import re

def ensure_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(rgb):
    return '#{:02X}{:02X}{:02X}'.format(rgb[0], rgb[1], rgb[2])

def find_font(font_name):
    # Get the script's directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Define the font path relative to the script
    font_path = os.path.join(script_dir, 'fonts', font_name)
    
    if os.path.exists(font_path):
        return font_path
    else:
        print(f"Warning: Could not find font at {font_path}")
        return None

def calculate_middle_colors(start_color, end_color):
    start_rgb = hex_to_rgb(start_color)
    end_rgb = hex_to_rgb(end_color)
    
    r_diff = end_rgb[0] - start_rgb[0]
    g_diff = end_rgb[1] - start_rgb[1]
    b_diff = end_rgb[2] - start_rgb[2]
    
    first_middle = (
        start_rgb[0] + r_diff // 3,
        start_rgb[1] + g_diff // 3,
        start_rgb[2] + b_diff // 3
    )
    
    second_middle = (
        start_rgb[0] + (r_diff * 2) // 3,
        start_rgb[1] + (g_diff * 2) // 3,
        start_rgb[2] + (b_diff * 2) // 3
    )
    
    return rgb_to_hex(first_middle), rgb_to_hex(second_middle)

def create_solid_background(width, height, color, output_file):
    if isinstance(color, str) and color.startswith('#'):
        color = hex_to_rgb(color)
    image = Image.new('RGB', (width, height), color)
    image.save(output_file, 'GIF')

def create_transparent_image(width, height, output_file):
    image = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    if output_file.lower().endswith('.gif'):
        image.save(output_file, 'GIF', transparency=0)
    else:
        image.save(output_file, 'PNG')

def create_transparent_image_with_text(width, height, text, font_name, font_size, text_color, letter_spacing, output_file, glow=False, y_offset=-12, x_offset=0, antialias=False):
    # Create base image
    image = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    
    # Set fontmode to force bilevel rendering if not using antialiasing
    if not antialias:
        draw.fontmode = "1"
    
    # Find font using relative path
    font_path = find_font(font_name)
    try:
        font = ImageFont.truetype(font_path if font_path else font_name, font_size)
    except Exception as e:
        print(f"Error loading font: {e}")
        font = ImageFont.load_default()
    
    if isinstance(text_color, str) and text_color.startswith('#'):
        main_color = hex_to_rgb(text_color)
    else:
        main_color = text_color
    
    # Split text into lines
    lines = text.split('\n')
    
    # Get font metrics
    ascent, descent = font.getmetrics()
    font_height = ascent + descent
    
    # Calculate maximum dimensions
    line_heights = []
    line_widths = []
    
    for line in lines:
        # Calculate dimensions for each line
        bbox = draw.textbbox((0, 0), line, font=font)
        line_width = bbox[2] - bbox[0] + (len(line) - 1) * letter_spacing
        line_height = bbox[3] - bbox[1]
        
        line_heights.append(line_height)
        line_widths.append(line_width)
    
    # Calculate total height needed
    total_height = sum(line_heights) + (len(lines) - 1) * (font_size // 2)  # Add spacing between lines
    
    # Calculate starting Y position to center all lines vertically
    start_y = (height - total_height) // 2 + y_offset
    current_y = start_y

    if glow:
        glow_color = (
            min(main_color[0] + 120, 255),
            min(main_color[1] + 120, 255),
            min(main_color[2] + 120, 255)
        )
        
        # Draw glow for each line
        for i, line in enumerate(lines):
            # Center this line horizontally
            start_x = (width - line_widths[i]) // 2 + x_offset
            
            # Draw text with glow
            if not antialias:
                draw.fontmode = "1"
            draw.text((start_x, current_y - 1), line, font=font, fill=glow_color + (25,),
                      spacing=letter_spacing)
            
            current_y += line_heights[i] + (font_size // 2)

    # Reset Y position for main text
    current_y = start_y
    
    # Draw each line
    for i, line in enumerate(lines):
        # Center this line horizontally
        start_x = (width - line_widths[i]) // 2 + x_offset
        
        # Draw text directly on the image
        if not antialias:
            draw.fontmode = "1"
        draw.text((start_x, current_y), line, font=font, fill=main_color + (255,),
                  spacing=letter_spacing)
        
        current_y += line_heights[i] + (font_size // 2)  # Move to next line with spacing
    
    # Save as GIF with transparency
    image.save(output_file, 'GIF', transparency=0)
      
def create_gradient(width, start_color, end_color, output_file, rtl=False):
    image = Image.new('RGB', (width, 1))
    
    start_rgb = hex_to_rgb(start_color)
    end_rgb = hex_to_rgb(end_color)
    
    r_step = (end_rgb[0] - start_rgb[0]) / (width - 1)
    g_step = (end_rgb[1] - start_rgb[1]) / (width - 1)
    b_step = (end_rgb[2] - start_rgb[2]) / (width - 1)
    
    for x in range(width):
        pos = width - 1 - x if rtl else x
        r = int(start_rgb[0] + (r_step * x))
        g = int(start_rgb[1] + (g_step * x))
        b = int(start_rgb[2] + (b_step * x))
        image.putpixel((pos, 0), (r, g, b))
    
    image.save(output_file, 'GIF')

def create_properties_file(color1, color2, color3, end_color, filename, is_root=False):
    if is_root:
        properties_content = '''#selfcare logo
selfcare.companyLogoImage = ../branding/branding_logo.png'''
    else:
        properties_content = f'''#splash header hex codes
splash.hex.code.1 = {end_color}
splash.hex.code.2 = {color3}
splash.hex.code.3 = {color2}

#header heading color
header.heading.color = {end_color}
header.navigation.color = #FFFFFF

# Go button color
header.go.font.color = #000000
header.go.background.color = #FFFFFF
header.go.border.color = #000000

#header links color
header.admin.color = #FFFFFF
header.hover.link.color = #FFFFFF

#splash header color
splash.username.color = #FFFFFF
splash.password.color = #FFFFFF
splash.login.back.ground.color = #FFFFFF
splash.login.text.color = #000000
splash.reset.back.ground.color = #FFFFFF
splash.reset.text.color = #000000

#splash content color
splash.header.color = #FFFFFF
splash.version.color = #FFFFFF'''

    with open(filename, 'w') as f:
        f.write(properties_content)

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Generate branding assets')
    parser.add_argument('--style', choices=['solid', 'gradient'], required=True,
                       help='Choose between solid or gradient style')
    parser.add_argument('--glow', action='store_true',
                       help='Add glow effect to the text')
    parser.add_argument('--start-color', default='#FFFFFF',
                       help='Starting color in hex format (e.g., #FFFFFF)')
    parser.add_argument('--end-color', default='#FF0000',
                       help='Ending color in hex format (e.g., #FF0000)')
    parser.add_argument('--logo-color',
                       help='Color for branding_logo.png text (e.g., #000000). If not specified, uses end-color')
    parser.add_argument('--antialias', action='store_true',
                        help='Enable anti-aliasing for text rendering (default: no)')
    args = parser.parse_args()

    # Validate hex colors
    color_pattern = re.compile(r'^#[0-9A-Fa-f]{6}$')
    if not color_pattern.match(args.start_color) or not color_pattern.match(args.end_color):
        parser.error("Colors must be in hex format (e.g., #FFFFFF)")
    if args.logo_color and not color_pattern.match(args.logo_color):
        parser.error("Logo color must be in hex format (e.g., #000000)")

    # Use logo_color if specified, otherwise fall back to end_color
    logo_color = args.logo_color if args.logo_color else args.end_color

    # Create directory structure
    branding_path = 'branding'
    ccmadmin_path = os.path.join(branding_path, 'ccmadmin')
    ensure_directory(branding_path)
    ensure_directory(ccmadmin_path)
    
    # Calculate middle colors using command line arguments
    start_color = args.start_color
    end_color = args.end_color
    middle_color1, middle_color2 = calculate_middle_colors(start_color, end_color)
    
    print(f"Using colors:")
    print(f"Start color: {start_color}")
    print(f"End color: {end_color}")
    print(f"Logo color: {logo_color}")
    print(f"Generated middle colors: {middle_color1}, {middle_color2}")
    
    # Create properties files
    create_properties_file(start_color, middle_color1, middle_color2, end_color, 
                         os.path.join(branding_path, 'BrandingProperties.properties'),
                         is_root=True)
    create_properties_file(start_color, middle_color1, middle_color2, end_color, 
                         os.path.join(ccmadmin_path, 'BrandingProperties.properties'),
                         is_root=False)
    
    # Create branding logo in branding folder with text
    create_transparent_image_with_text(
        44, 25,
        "AB",
        "m6x11.ttf",
        32,
        logo_color,
        0,
        os.path.join(branding_path, 'branding_logo.png'),
        glow=args.glow,
        y_offset=0,
        x_offset=1,
        antialias=args.antialias
    )
    
    if args.style == 'gradient':
        # Create gradient files
        create_gradient(652, start_color, middle_color1, 
                       os.path.join(ccmadmin_path, 'brandingHeaderBegLTR.gif'), rtl=False)
        create_gradient(652, middle_color1, middle_color2, 
                       os.path.join(ccmadmin_path, 'brandingHeaderMidLTR.gif'), rtl=False)
        create_gradient(652, middle_color2, end_color, 
                       os.path.join(ccmadmin_path, 'brandingHeaderEndLTR.gif'), rtl=False)
        
        # Create RTL versions
        create_gradient(652, start_color, middle_color1, 
                       os.path.join(ccmadmin_path, 'brandingHeaderBegRTL.gif'), rtl=True)
        create_gradient(652, middle_color1, middle_color2, 
                       os.path.join(ccmadmin_path, 'brandingHeaderMidRTL.gif'), rtl=True)
        create_gradient(652, middle_color2, end_color, 
                       os.path.join(ccmadmin_path, 'brandingHeaderEndRTL.gif'), rtl=True)
    else:  # solid style
        # Create solid background image
        create_solid_background(2048, 1, end_color, 
                              os.path.join(ccmadmin_path, 'brandingHeader.gif'))
    
    # Create logo with text using end_color
    create_transparent_image_with_text(
        44, 44,
        "Automate\nBuilders",
        "m3x6.ttf",
        20,
        end_color,
        -6,
        os.path.join(ccmadmin_path, 'ciscoLogo12pxMargin.gif'),
        glow=args.glow,
        y_offset=-2,
        x_offset=-20,
        antialias=args.antialias
    )

if __name__ == "__main__":
    main()