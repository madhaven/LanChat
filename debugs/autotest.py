from os import listdir, system
dirname='deb'
sock=input('Enter server python file : ')

files=listdir('.\\%s\\'%dirname)
for x in files:
    try:
        if x!='done':
            input('Testing %s'%x)
            system('start %s'%sock)
            system('start .\\%s\\%s'%(dirname, x))
            if 'y' not in input('press y to delete : '):
                system('move %s\\%s %s\\done'%(dirname, x, dirname))
            else: system('del %s\\%s'%(dirname, x))
    except Exception as e:input(print(x+' :', e))
