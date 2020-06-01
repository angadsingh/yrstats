from struct import unpack
from collections import namedtuple

# CONTRIBUTOR NEEDS FOR CONVERTING statparser.php to a python script!

def getFieldValue(ttl, data):
    response = {
        "raw": None,
        "val": None
    }

    if ttl.type == 1:
        v = unpack("c", data)
        response['val'] = v[1]

    if ttl.type == 2:
        v = unpack("?", data)
        response['val'] = v

    if ttl.type == 3:
        v = unpack("h", data)
        response['val'] = v[1]

    if ttl.type == 4:
        v = unpack("H", data)
        response['val'] = v[1]

    if ttl.type == 5:
        v = unpack("l", data)
        response['val'] = v[1]

    if ttl.type == 6:
        v = unpack("L", data)
        response['val'] = v[1]

    if ttl.type == 7:
        ttl.length -= 1
        v = unpack(ttl.length + "s", data)
        response['val'] = v

    if ttl.type == 20:
        response['val'] = None
        response['raw'] = data[0:ttl.length]

    return response

def processStatsDmp(file):
    with open(file, "rb") as f:
        data = f.read(4)
        
        if not data:
            return "Error"

        pad = 0
        result = {}

        while True:
            data = f.read(8)
            if not data:
                break

            import pdb; pdb.set_trace()
            TTL = namedtuple('TTL', 'tag type length')
            ttl = TTL._make(unpack('4sHH', data))
            pad = 4 - (ttl.length % 4) if ttl.length % 4 else 0
            print(str(ttl) + ", pad: " + str(pad))

            if ttl.length > 0:
                data = f.read(ttl.length)

                if pad > 0:
                    f.read(pad)

                fieldValueArr = getFieldValue(ttl, data)
                print(fieldValueArr)

                result[ttl.tag] = {
                    "tag": ttl.tag,
                    "length": ttl.length,
                    "raw": fieldValueArr['raw'],
                    "value": fieldValueArr['val']
                }
        print(result)

if __name__ == '__main__':
    processStatsDmp("C:\Program Files (x86)\Origin Games\Command and Conquer Red Alert II\stats.dmp")