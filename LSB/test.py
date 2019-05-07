from PIL import Image

text = 'namtran'
text = [bin(ord(t))[2:] for t in text]
print(text)
text = ["0" * (8 - len(t)) + t if len(t) < 8 else t for t in text]

print(text)

image = Image.open('spongebob.png')
pixels = image.load()

compo = bin(pixels[0, 0][0])
print(bin(pixels[0, 0][0]))
compo = list(compo)
print(compo)
compo.pop()
print(compo)
compo.append('0')
print(compo)
compo = ''.join(compo)
print(compo)
