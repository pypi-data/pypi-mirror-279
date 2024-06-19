def  multiplication_table(start: int = 1 , end: int = 5) -> None:
    for i in range(start,end+1):
        print(f'multiplication_table for {i} ↓')
        print()
        for j in range(1,11):
            print(f'{i}*{j} : {i*j}')
        print()

def fahrenheit_to_celsius(fahrenheit_temperatures : int) -> str:
    celsius = (fahrenheit_temperatures - 32) * 5 / 9
    return f'Fahrenheit {fahrenheit_temperatures} -> Celsius : {celsius:.2f}'

def celsius_to_fahrenheit(celsius : int) -> str:
    fahrenheit = (celsius * 9/5) + 32
    return f'Celsius {celsius} -> fahrenheit : {fahrenheit:.2f}'

def finds_the_longest_word(sentence: str) -> str:
    longest_word = [word for word in sentence.split() if len(word) == len(max(sentence.split(),key=len))][0]
    return f'The longest word is : {longest_word}'
