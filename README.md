# qrparse - QR code parser for python

This is a work in progress project and is not expected to work 100% of the time.

It only works with **21*21** QR codes (smallest possible).
This is not a scanner but rather a parser!

Also, **error correction is currently not supported**.

Usage
------

Put `qr.py` in the same directory as the source file. Call it like this:


```python
from qr import QR
QR(function).text
```

`x` and `y` are passed to `function` which must return a boolean indicating whether the pixel of the QR code is black.

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
except Exception as e:
	print("QR code could not be parsed: " + str(e))

```



```python
from qr import QR
from PIL import Image
im = Image.open("qr.png")

def isPixelBlack(x, y):
  r, g, b = im.getpixel((x, y))
  return r + g + b == 0

try :
	qr = QR(isPixelBlack)
	print(qr.text)
except Exception as e:
	print("QR code could not be parsed: " + str(e))

```


[*LICENSE*](https://github.com/TheSiki24/qrparse/blob/master/LICENSE)
