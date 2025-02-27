from itertools import product

letters = ['А', 'Я', 'Н', 'С', 'Т']
valid_count = 0
for code in product(letters, repeat=6):
    vowels=code.count('А')+code.count('Я')
    if (code.count('А'))==1 and(code.count('Я'))==1:
        valid_count+=1
print(valid_count)