
class Polynomial:
    def __init__(self, *args, **kwargs):

        input_value = list(args)
        self.list_pol = input_value

        if isinstance(kwargs, dict):
            if kwargs != {}:
                val_dict = kwargs

                for item in kwargs.items():
                    self.list_pol.append(item)
                self.list_pol = sorted(self.list_pol, key=lambda x: (x[0], x[1]))

                maximum = int(self.list_pol[-1][0][1:])

                for i in range(0, maximum + 1):
                    key = "x" + str(i)
                    if key not in val_dict:
                        val_dict[key] = 0

                new_lst = []

                for item in val_dict.items():
                    new_lst.append(item)
                new_lst = sorted(new_lst, key=lambda x: (x[0], x[1]))

                self.list_pol.clear()
                for value in new_lst:
                    self.list_pol.append(value[1])

        if isinstance(self.list_pol[0], list):
            self.list_pol = self.list_pol[0]

        if all([val == 0 for val in self.list_pol ]):
            self.list_pol = [0]

    def convert_to_equation(self):
        converted_string = ""
        list_copy = self.list_pol[:]
        position = len(list_copy)-1
        first_num = True

        if self.list_pol == [0]:
            return "0"

        for num in reversed(list_copy):
            if num != 0:

                if num == 1 and position != len(list_copy)-1:
                    converted_string += "+ "

                elif num > 0 and position != len(list_copy)-1 and not first_num:
                    converted_string += "+ " + str(num)

                elif num < 0:
                    if position == len(list_copy)-1:
                        converted_string += str(num)[0]
                    elif num == -1 and position != 0:
                        converted_string += str(num)[0] + " "
                    else:
                        converted_string += str(num)[0] + " " + str(num)[1:]

                elif num != 1:
                    converted_string += str(num)
                first_num = False

                if position >= 0:
                    if position > 1:
                        converted_string += "x^" + str(position) + " "
                    elif position == 0 and num == 1:
                        converted_string += str(num)
                    elif position > 0:
                        converted_string += "x" + " "

            position -= 1

        if converted_string[-1] == " ":
            converted_string = converted_string[:-1]
        return converted_string

    def converter(self, lst):
        val_dict = dict([(x, 0) for x, _ in lst])  # setting each coefficient to 0
        for i, val in lst:
            val_dict[i] += val  # adding values to each coefficient
        lst = list(map(tuple, val_dict.items()))  # converting a dictionary back into a list
        lst = list(map(lambda x: x[1], lst))  # removing coefficients
        return lst

    def power(self, pol, power):
        new_lst = []
        pol2 = pol
        for k in range(power - 1):
            for val, i in enumerate(pol):
                for val2, j in enumerate(pol2):  # new_lst = [(val + val2, i*j) for val, i in enumerate(pol) for val2, j in enumerate(pol)]
                    new_lst.append((val + val2, i * j))
            pol2 = self.converter(new_lst)
            new_lst.clear()
        new_pol = Polynomial(pol2)
        return new_pol

    def at_value(self, x):
        answer = self.list_pol[0]
        for i in range(1, len(self.list_pol)):
            answer += self.list_pol[i] * (x ** i)
        return answer

    def derivative(self):
        new_pol = []
        for i in range(1, len(self.list_pol)):
            new_pol.append(i * self.list_pol[i])
        new_pol = Polynomial(new_pol)
        return new_pol

    def __str__(self):
        return self.convert_to_equation()

    def __eq__(self, other):
        if isinstance(other, Polynomial):
            return self.list_pol == other.list_pol
        return False

    def __pow__(self, other):
        if isinstance(other, int):
            return self.power(self.list_pol, other)

    def __add__(self, other):
        if isinstance(other, Polynomial):
            max_len = max(len(self.list_pol), len(other.list_pol))
            self.list_pol += [0] * (max_len - len(self.list_pol))
            other.list_pol += [0] * (max_len - len(other.list_pol))
            new_pol = Polynomial([x + y for x, y in zip(self.list_pol, other.list_pol)])
        else:
            raise ValueError("One of the inputs is not a polynomial")
        return new_pol.convert_to_equation()

print(str(Polynomial(4,34,3,4 ** 7).at_value(3)))


assert str(Polynomial(0, 1, 0, -1, 4, -2, 0, 1, 3, 0)) == "3x^8 + x^7 - 2x^5 + 4x^4 - x^3 + x"
assert str(Polynomial([-5,1,0,-1,4,-2,0,1,3,-1])) == "-x^9 + 3x^8 + x^7 - 2x^5 + 4x^4 - x^3 + x - 5"
assert str(Polynomial(x2=0)) == "0"
assert str(Polynomial(x0=0)) == "0"
assert str(Polynomial([-1,1,1,0])+Polynomial(1,-1,1)) == "2x^2"
assert str(Polynomial(x0=2).derivative()) == "0"
assert Polynomial(-2, 3, 4, -5).at_value(0) == -2
assert str(Polynomial(x3=2,x1=3,x0=2).derivative().derivative()) == "12x"