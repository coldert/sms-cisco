mask = 24
bits = 0
for i in xrange(32-mask,32):
	bits |= (1<<i)
print "%d.%d.%d.%d" % ((bits & 0xff000000) >> 24, (bits & 0xff0000) >> 16, (bits & 0xff00) >> 8, (bits & 0xff))

