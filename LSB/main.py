import bitarray
import base64
from PIL import Image

msg = "YourVerySecret"
encoded_msg = base64.b64encode(msg)

# print encode_msg
ba = bitarray.bitarray()
ba.frombytes(encoded_msg.encode('utf-8'))
bit_array = [int(i) for i in ba]

#
im = Image.open("spongebob.png")
im.save("lsb_spongebob.png")

im = Image.open("lsb_spongebob.png")
width, height = im.size
pixels = im.load()

i = 0
for x in range(0, width):
    r, g, b = pixels[x, 0]
    print("[+] Pixel : [%d,%d] = (%d,%d,%d)" % (x, 0, r, g, b))

    new_bit_red_pixel = 255
    new_bit_green_pixel = 255
    new_bit_blue_pixel = 255

    if i < len(bit_array):
        r_bit = bin(r)
        r_last_bit = int(r_bit[-1])
        r_new_last_bit = r_last_bit & bit_array[i]
        new_bit_red_pixel = int(r_bit[:-1] + str(r_new_last_bit), 2)
        i += 1

    if i < len(bit_array):
        # Green pixel
        g_bit = bin(g)
        g_last_bit = int(g_bit[-1])
        g_new_last_bit = g_last_bit & bit_array[i]
        new_bit_green_pixel = int(g_bit[:-1] + str(g_new_last_bit), 2)
        i += 1

    if i < len(bit_array):
        # Blue pixel
        b_bit = bin(b)
        b_last_bit = int(b_bit[-1])
        b_new_last_bit = b_last_bit & bit_array[i]
        new_bit_blue_pixel = int(b_bit[:-1] + str(b_new_last_bit), 2)
        i += 1

    pixels[x, 0] = (new_bit_red_pixel, new_bit_green_pixel, new_bit_blue_pixel)
    print("[+] \tAfter: (%d,%d,%d)" % (new_bit_red_pixel, new_bit_green_pixel, new_bit_blue_pixel))

im.save("lsb_spongebob.png")
