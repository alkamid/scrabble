#convert OSPS to Zyzzyva format

with open('osps-baseforms.txt') as f, open('OSPS-Zyzzyva.txt', 'w') as g:
    temp_infl = ''
    for line in f.readlines():
        words = line.split()
        if temp_infl == '':
            temp_infl = words[0]
            temp = []
        elif temp_infl != words[0]:
            g.write(temp_infl)
            for i, word in enumerate(temp):
                if i > 0:
                    if temp[i-1]['base'] == None:
                        g.write(' []')
                    g.write(' /')
                if len(temp) > 1 and word['base'] == None:
                    g.write(' ' + temp_infl)
                elif word['base'] != None:
                    g.write(' <' + word['base'] + '>')
                if word['def'] != None:
                    g.write(' ' + word['def'])
            g.write('\n')
            temp_infl = words[0]
            temp = []

        tempdict = {}
        if words[1].upper() != words[0]:
            tempdict['base'] = words[1]
        else:
            tempdict['base'] = None
        if len(words) > 2:
            tempdict['def'] = words[2]
        else:
            tempdict['def'] = None
        temp.append(tempdict)

        temp_infl = words[0]
        
