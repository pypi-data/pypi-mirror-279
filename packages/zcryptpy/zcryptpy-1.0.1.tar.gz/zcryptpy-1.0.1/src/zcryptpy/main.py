def zencrypt_narrated(string):
    tstr = string.upper()
    print(f"Input: '{string}' (converted to uppercase ({tstr}) for compatibility reasons)")
    dtemp = [ord(i) for i in tstr]
    print("Converted to Decimal list: " + str(dtemp))
    modtmp = [((2*i)+j+1) for j, i in enumerate(dtemp)]
    print("Shifted values up: " + str(modtmp))
    htemp = [hex(i).replace("0x","") for i in modtmp]
    print("Covnerted to hexadecimal: " + str(htemp))
    hrtmp = list(reversed(htemp))
    print("Reversed value order: " + str(hrtmp))
    hrstr = ''.join(hrtmp)
    print(f"Converted to string: '{hrstr}'")
    prefix = hex(4*len(hrstr)).replace("0x","").zfill(2)
    print(f"Adding checksum prefix '{prefix}' to string")
    result = prefix + "-" + hrstr
    print(f"Done! Output: '{result}'")
    return result

def zencrypt(string):
    tstr = string.upper()
    dtemp = [ord(i) for i in tstr]
    modtmp = [((2*i)+j+1) for j, i in enumerate(dtemp)]
    htemp = [hex(i).replace("0x","") for i in modtmp]
    hrtmp = list(reversed(htemp))
    hrstr = ''.join(hrtmp)
    prefix = hex(4*len(hrstr)).replace("0x","").zfill(2)
    result = prefix + "-" + hrstr
    return result

def zdecrypt(string):
    spl = string.split("-")
    cstr = spl[1]
    temp = list(map(''.join, zip(*[iter(cstr)]*2)))
    rtemp = list(reversed(temp))
    dtemp = [int(i,16) for i in rtemp]
    sdtmp = [int((i-j-1)/2) for j, i in enumerate(dtemp)]
    ctemp = [chr(i) for i in sdtmp]
    result = ''.join(ctemp)
    return result

def zdecrypt_narrated(string):
    print(f"Input: '{string}'")
    spl = string.split("-")
    print("Separated prefix: " + str(spl))
    cstr = spl[1]
    print("Removed prefix: " + cstr) 
    temp = list(map(''.join, zip(*[iter(cstr)]*2)))
    print("Split to bytes: " + str(temp))
    rtemp = list(reversed(temp))
    print("Reversed value order: " + str(rtemp))
    dtemp = [int(i,16) for i in rtemp]
    print("Converted to decimal: " + str(dtemp))
    sdtmp = [int((i-j-1)/2) for j, i in enumerate(dtemp)]
    print("Shifted values down: " + str(sdtmp))
    ctemp = [chr(i) for i in sdtmp]
    print("Converted to ASCII: " + str(ctemp))
    result = ''.join(ctemp)
    print(f"Converting to string...Done! Output: '{result}'")
    return result
