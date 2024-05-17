from PIL import Image, ImageDraw
import numpy as np
import easyocr

def get_text(pil_image):
    reader = easyocr.Reader(['en', 'ar'])
    draw = ImageDraw.Draw(pil_image)
    
    result = reader.readtext(np.array(pil_image))
    text_output = ""
    
    for detection in result:
        bbox = detection[0]
        text = detection[1]
        text_output += text + " "
        score = detection[2]
        print(text, score)
        
        top_left = tuple(map(int, bbox[0]))
        bottom_right = tuple(map(int, bbox[2]))
        draw.rectangle([top_left, bottom_right], outline=(0, 255, 0))
    
    return text_output, pil_image

if __name__ == "__main__":
    path = "img.png"
    pil_image = Image.open(path)
    
    out, processed_image = get_text(pil_image)
    print(out)
    processed_image.show()
    processed_image.save("output_image.png")
