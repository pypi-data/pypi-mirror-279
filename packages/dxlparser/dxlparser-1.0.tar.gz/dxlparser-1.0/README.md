# dxf-parser

## Ejemplo de uso

```
import pricelang
originalExpression = "all: 1200; unam: 500, +15%[f>=2023-12-1 & f<=2023-12-31], +200[n>=3&x>=2000]; general: 800, +50%[f=--2-14]"
# Parsing the expression string to PriceTree representation
tree = pricelang.parse(originalExpression)
tree.show()
print(tree)
# Interpreting an expression tree
conditions = {
    "f": "2023-12-20",
    "n": 5,
    "x": 3000.40,
    "user": "unam",
}
price = pricelang.test(tree, conditions)
print(price)
```