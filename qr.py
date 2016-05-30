
masks = [
	lambda c, r: (r + c) % 2 == 0,
	lambda c, r: r % 2 == 0,
	lambda c, r: c % 3 == 0,
	lambda c, r: (r + c) % 3 == 0,
	lambda c, r: (r // 2 + c // 3) % 2 == 0,
	lambda c, r: (r * c) % 2 + (r * c) % 3 == 0,
	lambda c, r: ((r * c) % 3 + r * c) % 2 == 0,
	lambda c, r: ((r * c) % 3 + r + c) % 2 == 0
]

ec_count = [
	10, 7, 17, 13
]

ec_name = "MLHQ"

len_count = {
	1: 10,
	2: 9,
	4: 8,
	8: 8
}

alphanumeric_charmap = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ $%*+-./:"

def stringToBools(s):
	return [c == "1" for c in s]

def boolsToString(data):
	return "".join(["1" if b else "0" for b in data])

def xor(d1, d2):
	assert len(d1) == len(d2)

	ret = []
	for i in range(0, len(d1)):
		ret.append(d1[i] != d2[i])

	return ret


def boolsToInt(data):
	val = 0
	for d in data:
		val = val << 1 | d

	return val

class QR:
	def get(self, x, y):
		return self.qr(x, y) != self.mask(x, y)

	def getMask(self):
		return boolsToInt(self.format[2:5])

	def getECLevel(self):
		return boolsToInt(self.format[0:2])

	def getFormat(self):
		format1 = []
		for y in range(0, 6):
			format1.append(self.get(8, y))

		format1.append(self.get(8, 7))
		format1.append(self.get(8, 8))
		format1.append(self.get(7, 8))

		for x in range(0, 6):
			format1.append(self.get(5 - x, 8))

		format2 = []
		for x in range(0, 8):
			format2.append(self.get(20 - x, 8))

		for y in range(0, 7):
			format2.append(self.get(8, 14 + y))

		# print(format1)
		# print(format2)
		# exit()

		assert format1 == format2

		return xor(list(reversed(format1)), stringToBools("101010000010010"))

		# list(reversed(format1))
		# ich habe den kack falschrum implementiert... nvm


	def getLine(self, x, y_start, y_end):
		assert y_start != y_end
		data = []

		if y_start < y_end: # DOWN
			for y in range(y_start, y_end):
				data.append(self.get(x + 1, y))
				data.append(self.get(x + 0, y))
		else:				# UP
			diff = y_start - y_end
			for y in range(0, diff):
				data.append(self.get(x + 1, y_end + (diff - 1) - y))
				data.append(self.get(x + 0, y_end + (diff - 1) - y))

		return data

	def readDataStream(self):
		data = []
		data += self.getLine(19, 21, 9)
		data += self.getLine(17, 9, 21)
		data += self.getLine(15, 21, 9)
		data += self.getLine(13, 9, 21)
		data += self.getLine(11, 21, 7)
		data += self.getLine(11, 6, 0)
		data += self.getLine(9, 0, 6)
		data += self.getLine(9, 7, 21)
		data += self.getLine(7, 13, 9)
		data += self.getLine(4, 9, 13)
		data += self.getLine(2, 13, 9)
		data += self.getLine(0, 9, 13)
		return data

	def decode(self):
		state = "enc"
		encoding = 0
		length = -1
		i = 0
		out = ""
		reading = 0

		while True:
			if state == "enc":
				encoding = boolsToInt(self.data[i:i + 4])
				i += 4
				state = "len"
				if encoding == 0:
					break

				# print("encoding " + str(encoding))
			elif state == "len":
				length = boolsToInt(self.data[i:i + len_count[encoding]])
				reading = 0
				i += len_count[encoding]
				state = "read"
				# print("length " + str(length))

			elif state == "read":
				if reading == length:
					state = "enc"
					continue

				if encoding == 0b0100:
					out += chr(boolsToInt(self.data[i:i + 8]))
					i += 8
					reading += 1

				elif encoding == 0b0010:
					if reading == length - 1 and length % 2 == 1:
						c = boolsToInt(self.data[i:i + 6])
						i += 6
						out += alphanumeric_charmap[c]
						reading += 1
					else:
						d = boolsToInt(self.data[i:i + 11])
						c1 = d // 45
						c2 = d - c1 * 45
						out += alphanumeric_charmap[c1] + alphanumeric_charmap[c2]
						i += 11
						reading += 2
				else:
					raise Exception("TODO")

		return out


	def __init__(self, qr_param):

		self.qr = qr_param
		self.mask = lambda x, y: False

		self.format = self.getFormat()
		# print("format " + boolsToString(self.format))

		self.mask = masks[self.getMask()]
		# print("mask " + str(self.getMask()))

		self.ec_level = self.getECLevel()
		# print("ec " + str(self.ec_level))

		self.data = self.readDataStream()
		self.text = self.decode()

		# print(self.text)

# print(boolsToString(stringToBools("110011000101111")))
# print(boolsToString(xor(stringToBools("110011000101111"), stringToBools("101010000010010"))))

# f = xor(stringToBools("110011000101111"), stringToBools("101010000010010"))
# print(f[0:2])
# c = boolsToInt(f[0:2])
# print("ec: " + str(c) + " " + ec_name[c])

# print("mask: " + str(boolsToInt(f[2:5])))