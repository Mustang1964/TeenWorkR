import struct

def get_image_info(data):
    size = len(data)
    height = -1
    width = -1
    content_type = ''

    # JPEG
    if data[:2] == b'\xff\xd8':
        content_type = 'image/jpeg'
        b = data
        try:
            w, h = -1, -1
            idx = 2
            while idx < len(b):
                if b[idx] == 0xff:
                    marker = b[idx+1]
                    if marker >= 0xc0 and marker <= 0xc3:
                        h, w = struct.unpack(">HH", b[idx+5:idx+9])
                        break
                    else:
                        length = struct.unpack(">H", b[idx+2:idx+4])[0]
                        idx += length + 2
                else:
                    idx += 1
            width, height = w, h
        except:
            pass
    # PNG
    elif data[:8] == b'\x89PNG\r\n\x1a\n':
        content_type = 'image/png'
        w, h = struct.unpack('>LL', data[16:24])
        width, height = w, h
    
    return width, height, content_type

with open('favicon.jpeg', 'rb') as f:
    w, h, t = get_image_info(f.read())
    print(f"favicon.jpeg: {w}x{h} ({t})")

with open('favicon.png', 'rb') as f:
    w, h, t = get_image_info(f.read())
    print(f"favicon.png: {w}x{h} ({t})")
