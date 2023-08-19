# count = 1
# while True:
#     try:
#         if count == 5:
#             raise TypeError
#         print(1)
#         count += 1
#     except:
#         break

# https://cars.av.by/citroen/c5/filter?brands%5B0%5D%5Bbrand%5D=43&brands%5B0%5D%5Bmodel%5D=181&price_currency=2&page=2
# https://cars.av.by/citroen/c5/filter?brands[0][brand]=43&brands[0][model]=181&page=2
# https://cars.av.by/filter?brands[0][brand]=43&brands[0][model]=181&page=2


# a = 'https://cars.av.by/filter?brands%5B0%5D%5Bbrand%5D=1216&brands%5B0%5D%5Bmodel%5D=5908&price_currency=2&page=2'
# b = a.replace('brands%5B0%5D%5Bbrand%5D', 'brands[0][brand]').replace('%5B0%5D%5Bmodel%5D', '[0][model]')\
#     .replace('price_currency=2&', '')
# print(b)

# https://cars.av.by/filter?brands%5B0%5D%5Bbrand%5D=1216&brands%5B0%5D%5Bmodel%5D=5908&price_currency=2&page=2


# try:
#     print(1/0)
# except:
#     print(2)

# a = {'a': [1,2,3],
#      'b':[3,22,2],
#      'c': [77,4,56]}
# a = [(10, 12), (2, 45), (1, 67), (3, 2)]
# a.sort(key=lambda i: i[1])
# print(a)

# a = [i for i in range(1, 10+1)]
# for i in a: print(i)

# a = [i for i in range(1,10)]
# print(a)
# b = a.index(2)
# print(b)
# for i in range(10):
#     a = 12 + i
# print(i)