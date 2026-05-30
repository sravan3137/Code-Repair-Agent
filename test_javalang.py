import javalang
code = """
package com.ex;
class User {
    User(String a) {}
    void foo() { new User("x"); }
}
"""
tree = javalang.parse.parse(code)
for c in tree.types:
    for m in c.constructors:
        print(m.name, type(m))
for path, node in tree.filter(javalang.tree.ClassCreator):
    print("ClassCreator:", node.type.name)
