def check(p):
  last_char = p[0]
  for c in p[1:]:
    if c < last_char:
      return False
    last_char = c

  for i in range(0,10):
    if len(list(filter(lambda x: x == str(i), p))) == 2:
      return True
  return False


count = 0

for p in range(236491,713787):
  
  if check(str(p)):
    count += 1



print(count)
  
