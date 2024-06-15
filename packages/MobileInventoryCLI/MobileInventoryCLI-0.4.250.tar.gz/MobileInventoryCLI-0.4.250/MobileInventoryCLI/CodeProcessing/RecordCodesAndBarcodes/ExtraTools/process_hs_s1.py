import re,csv
from colored import Fore,Style

errors={'too many':[],'too few':[]}
rows=[['Term','Definition']]

with open("dictionary.txt","r") as f:
    for num,line in enumerate(f.readlines()):
        p=re.findall(r"#PAGE#\d*#START#",line)
        if len(p) > 0:
            continue
        elif line in ['','\n']:
            continue
        else:
            if '#' in line:
                print(line.replace('#',f'{Fore.light_red}#{Style.reset}'))
                if len(line.split('#')) > 2:
                    print(f"{Fore.orange_red_1}Too many '#' {line}{Style.reset}")
                    errors['too many'].append({'line no.':num+1,'count':len(line.split('#')),'line text':line})
            else:
                print(f"{Fore.orange_red_1}Missing '#'{line}{Style.reset}")
                errors['too few'].append({'line no.':num+1,'count':len(line.split('#')),'line text':line})

            rows.append(line.split("#"))



for k in errors:
    for kk in errors[k]:
        print(f'{Fore.light_red}{k}{Style.reset}',kk)
    #print(rows)
    
with open("result.hsv","w") as ofile:
    writer=csv.writer(ofile,delimiter="#")
    writer.writerows(rows)

