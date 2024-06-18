def nearest_interger() -> str:
    x , y = map(int, input('enter the two numbers seperated by space : ').split())
    divisible_by_four = []
    for num in range(1,x+2):
        if num % y == 0:
            divisible_by_four.append(num)
    nearest = divisible_by_four[-1]
    return '{} is the nearest of {} because it is divisible by {}'.format(nearest , x , y)

print(nearest_interger())


