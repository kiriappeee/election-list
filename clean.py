import json
import os
import re

candidate_lists = os.listdir('./lists')
candidates = {}
number_of_candidates = 0
p = re.compile('^\d+ ')
for candidate_list in candidate_lists:
  district_number, district_name = candidate_list.split('_')[:2]
  details = open(f'./lists/{candidate_list}', 'r').read().strip()
  lines = details.splitlines()
  current_party = ''
  candidates[district_number] = {
    'name': district_name
  }
  for line in lines:
    if 'PARTY:' in line:
      current_party = line.split('PARTY: ')[1].strip()
      candidates[district_number][current_party] = []
    else:
      number_index = p.search(line)
      if not number_index:
        print(district_number, district_name, line)
        continue
      candidate_number = int(line[:number_index.end()-1].strip())
      candidate_name = line[number_index.end():].strip()
      number_of_candidates += 1
      candidates[district_number][current_party].append({
        'candidate_name': candidate_name,
        'candidate_number': candidate_number
      })

f = open('cleaned/candidates_full.json', 'w')
f.write(json.dumps(candidates, indent=2))
f.close()
print(number_of_candidates)