dirname='deb'
try:
    f=open('autogui.py', 'r')
    lines=[x for x in f]
    f.close()
    for x in range(len(lines)):
        f=open('%s\\test%.3d.pyw'%(dirname, x), 'w')
        for y in range(len(lines)):
            whitespaces=0
            if y==x:
                try:
                    if ':' not in lines[y][2:] and '#'!=lines[y][0]:
                        if lines[y][0]==' ':
                            for char in lines[y]:
                                if char==' ': whitespaces+=1
                                else :break
                        f.write(' '*whitespaces+'messagebox.showinfo(\'TEST\', \'BEFORE THELINE\')\n')
                        f.write(lines[y])
                        f.write(' '*whitespaces+'messagebox.showinfo(\'TEST\', \'AFTER THELINE\');exit()\n')
                        continue
                except:pass
            f.write(lines[y])
        f.close()
except Exception as e: input(e)
else: input('GUI.PY COPIED TO %s'%dirname)