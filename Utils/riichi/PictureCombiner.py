import io
import os

from html2image import Html2Image
from PIL import Image


def create_mahjong_hand(tile_urls, output_file="hand.png"):
    BG_URL = "https://raw.githubusercontent.com/FluffyStuff/riichi-mahjong-tiles/refs/heads/master/Regular/Front.svg"
    hti = Html2Image(custom_flags=['--default-background-color=00000000', '--hide-scrollbars'])

    html_content = """
    <html>
    <style>
        body { margin: 0; padding: 0; background: transparent; }
        .hand { display: flex; }
        .tile-container { position: relative; width: 66px; height: 90px; } 
        /* Adjust width/height above to match your actual SVG dimensions if needed */

        .bg { position: absolute; top: 0; left: 0; z-index: 1; width: 100%; height: 100%; }
        .glyph { position: absolute; top: 0; left: 0; z-index: 2; width: 100%; height: 100%; }
    </style>
    <body>
        <div class="hand">
    """

    for url in tile_urls:
        html_content += f"""
            <div class="tile-container">
                <img src="{BG_URL}" class="bg">
                <img src="{url}" class="glyph">
            </div>
        """

    html_content += "</div></body></html>"

    # blud man macht einfach einen fucking screenshot von html das man grad gebaut hat
    hti.screenshot(html_str=html_content, save_as=output_file, size=(1000, 200))

    img = Image.open(output_file)
    img = img.crop(img.getbbox())

    image_binary = io.BytesIO()
    img.save(image_binary, 'PNG')
    image_binary.seek(0)
    os.remove("hand.png")  # prevent one hand png always existing
    return image_binary
