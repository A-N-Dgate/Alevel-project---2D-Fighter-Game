class C:
    def m(self):
        return "result"

    def n(self):
        print("result")
    

an_object = C()

class_method = getattr(C, "n")
result = class_method(an_object)

#print(result)

#calling a method with no return statement also works
