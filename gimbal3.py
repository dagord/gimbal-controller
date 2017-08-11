from pysimplebgc import SimpleBGC32
device = SimpleBGC32.from_url('serial:/dev/ttyUSB1:115200:8N1')
device.getcmdlist()