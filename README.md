# qrparse - QR code parser for python

This is a work in progress project and is not expected to work 100% of the time.

It only works with **21*21** QR codes (smallest possible).
This is not a scanner but rather a parser!

Also, **error correction is currently not supported**.

Usage
------

put qr.py in same dir as source file

`QR(lambda x, y: bool).text`

Examples
--------

```python
from qr import QR

sample = [
	"#######    #  #######",
	"#     # ##  # #     #",
	"# ### #  # ## # ### #",
	"# ### # ##### # ### #",
	"# ### # ## #  # ### #",
	"#     #  #  # #     #",
	"####### # # # #######",
	"        ## ##        ",
	"## #### ##  ### ## # ",
	"# #### #    #### ### ",
	"  # # ##   #  ##     ",
	"# ## #   # ##   ##   ",
	"## ######## ### #####",
	"        #   #  # #   ",
	"#######  ##  ##  ####",
	"#     # # #  #  # ###",
	"# ### # ## #  #   ###",
	"# ### # # ###   # #  ",
	"# ### #  #    #    ##",
	"#     # ###  ###  ## ",
	"####### ## #       # "
]

try :
	qr = QR(lambda x, y: sample[y][x] == "#")
	print(qr.text)
except Exception, e:
	print("fuck this library... shits not working" + str(e))

```


----------


```python
from qr import QR
from PIL import Image
im = Image.open("qr.png").convert("RGB")

def isPixelBlack(x, y):
  r, g, b = im.getpixel((x, y))
  return r + g + b == 0

try :
	qr = QR(isPixelBlack)
	print(qr.text)
except Exception, e:
	print("fuck this library... shits not working" + str(e))

```


[*LICENSE*](https://github.com/TheSiki24/qrparse/blob/master/LICENSE)
