from django.test import TestCase


# Create your tests here.


def snake_to_camel_string(snake_str):
    ret = snake_str.split("_")
    li = []
    n = len(ret)
    li.append(ret[0])
    for i in ret[1:]:
        j = i.capitalize()
        li.append(j)
    ret = "".join(li) + str(n)
    return ret


print(snake_to_camel_string("i_am_a_snake"))
print(snake_to_camel_string("king_of_the_world"))
print(snake_to_camel_string("pretty"))
