import re

f = open('candidates.txt', 'r')
a = f.read()
f.close()
#print(a)

remove_regex = re.compile('^Name of each|^and the distinguishing|^Independent Group and each Independent Group|I fldgi|GAZETTE EXTRAORDINARY|^\d+ A$|^\d+A$|\(Cont\.|\(Contd|2020\.06\.09|^distinguishing number of each Recognized Political| Nomination Paper')

party_line_regex = re.compile("^[a-zA-Z\s’']+\d")
independent_party_regex = re.compile('^Independent Group \d+ \d|^Independant Group \d+ \d')
trailing_name_regex = re.compile('^[A-Za-z\s]+$')
lines = a.split('\n')
count = 0
while count < len(lines):
  line = lines[count]
  if remove_regex.search(line):
    lines.pop(count)
  else:
    count += 1

count = 0
party_list = []
while count < len(lines):
  line = lines[count]
  party_line_result = party_line_regex.search(line)
  if party_line_result:
    independent_line_result = independent_party_regex.search(line)
    if independent_line_result:
      candidate_section = line[independent_line_result.end()-1:].strip()
      party_section = line[independent_line_result.start():independent_line_result.end()-1].strip()
    else:
      candidate_section = line[party_line_result.end()-1:].strip()
      party_section = line[party_line_result.start():party_line_result.end()-1].strip()
    lines[count] = f'PARTY: {party_section}'
    party_list.append(party_section)
    lines.insert(count+1, candidate_section)
  else:
    if trailing_name_regex.search(line) and line not in party_list:
      lines[count-1] = f'{lines[count-1]} {lines[count]}'
      lines.pop(count)
      count -= 1
    if line in party_list:
      lines.pop(count)
      count -= 1
  count += 1
print('\n'.join(lines))