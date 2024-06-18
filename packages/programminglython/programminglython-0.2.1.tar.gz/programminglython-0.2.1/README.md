[![status workflow test](https://github.com/guangrei/lython/actions/workflows/python-app.yml/badge.svg)](https://github.com/guangrei/lython/actions) 
[![status workflow build](https://github.com/guangrei/lython/actions/workflows/release_to_pypi.yml/badge.svg)](https://github.com/guangrei/lython/actions)
[![Downloads](https://static.pepy.tech/badge/programminglython)](https://pepy.tech/project/programminglython)
[![Code style: black ]( https://img.shields.io/badge/code%20style-black-000000.svg )](https://github.com/psf/black)

example lython code

```python
def test(num)
    for i in range(num) do
        if i == 0 then
            print("zero")
        elif i % 2 == 1 then
            print("odd")
        else
            print("even")
        end # if else
    end # for
end # def

test(10)
```

Note:

- The indentation in the code above is just to make the code look pretty and has no effect on the parser.

- you cant use `then`, `do`, `end` as name variable, function and class in lython.

github: [guangrei/lython](https://github.com/guangrei/lython)
