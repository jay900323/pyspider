class TestClass(object):
    val1 = 100
 
    def __init__(self):
        self.val2 = 200
     
    def fcn(self,val = 400):
        val3 = 300
        self.val4 = val
        self.val5 = 500
if __name__ == '__main__':
    inst = TestClass()
      
    print TestClass.val1
    print inst.val1
    print inst.val2
    #   print inst.val3
    print inst.val4  
    print inst.val5