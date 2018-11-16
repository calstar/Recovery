#!/usr/bin/env python3
import sys, os
import zipfile
import xml.etree.ElementTree as et
import xml.dom.minidom as xdm
import time
import matplotlib.pyplot as plt
def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = et.tostring(elem, 'utf-8')
    reparsed = xdm.parseString(rough_string)
    return reparsed.toprettyxml(indent="\t")

def main():
	zf = zipfile.ZipFile(sys.argv[1], 'r')

	#print("files: " + str(zf.namelist()))
	#print("loading rocket.ork ...")

	'''
	# Time XDM parsing. About .08 for SV6
	start = time.time()
	for i in range(10 ** 2):
		raw_xml = xdm.parseString(zf.read('rocket.ork'))
	end = time.time()
	print("XDM parse:", end - start)

	# Time XDM prettyprinting. About .05 for SV6
	start = time.time()
	for i in range(10 ** 2):
		raw_pp = raw_xml.toprettyxml()
	end = time.time()
	print("XDM pretty print:", end - start)

	# Time ET parsing. About .025 for SV6
	start = time.time()
	for i in range(10 ** 2):
		ork = et.fromstring(zf.read('rocket.ork'))
	end = time.time()
	print("ET parse:", end - start)
	'''

	# Get raw xml of ork file
	raw_xml = xdm.parseString(zf.read('rocket.ork'))
	# Pretty print xml or ork file
	raw_pp = raw_xml.toprettyxml()
	print(raw_pp)
	# Create ElementTree of ork file
	ork = et.fromstring(zf.read('rocket.ork'))
	#print(ork)
	# Printing stuff
	#print(ork.tag, 'contains:', list(ork))
	# Newline
	#print('')
	rocket = ork.find('rocket')
	motorconfiguration = rocket.find('motorconfiguration')
	#print(rocket, motorconfiguration)
	#print(motorconfiguration.text)
	#for item in motorconfiguration.iter():
#		print(item)


#	print("*******")
	# Print more stuff
	#for element in list(ork):
	#	print(element.tag, 'contains:', list(element))
#		print()
	#print(list(ork.find('simulations').find('simulation')))
	#print(list(ork.find('rocket').find('subcomponents').find('stage')))
	#print(prettify(ork.find('rocket')))
	sum = 0
	mass = []
	time = []
	for item in ork.iter():
		if(item.tag != 'datapoint'):
			if(item.tag == 'databranch'):
				print(len(mass))
			pass
		else:
			#print(item.text)
			time_val = item.text.split(',')[0]
			mass_val = item.text.split(',')[19]
			#print(mass_val)
			time.append(float(time_val))
			mass.append(float(mass_val))
			if(item.tag == 'mass' or item.tag == 'overridemass'): # or item.tag == 'masscomponent')
				print(item.tag)
				print(float(item.text))
				sum += float(item.text)
	#print(sum)
	#print(mass)
	print(len(mass))
	plt.plot(time[:888], mass[:888])
	#plt.plot(mass[888:1682])
	#plt.plot(time[1682:2476], mass[1682:2476])
	plt.plot(time[2476:2982], mass[2476:2982])
	plt.show()
	#rocket = xml.find('rocket')
	#print("rocket:")
	#print("  name: "		+ rocket.find('name').text)
	#print("  referencetype: "		+ rocket.find('referencetype').text)
	#print(list(rocket.find('subcomponents')))
	#for config in rocket.findall('motorconfiguration'):
	#	print(list(config))
	#stage = rocket.find('stage') #wht?
	#print(list(rocket))

if __name__ == '__main__':
	main()