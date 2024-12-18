    def formula_reset(self):
        self.operator=Formula.operator[random.randint(0,3)]
        if self.operato=='*'|self.operato=='/':
               self.value=random.uniform(0,2)
        else:            
            self.value=random.randint(1,10)
        self.position_Y=-50
        self.text=f"{self.operator}{self.value}"
        
    class heap():
        heap_size=0
        array=[]
        array_max_5=[]
         @staticmethod
        def heapify(index):
            while heap.array[index]<max(heap.array[2*index+1],heap.array[2*index+2]):
                temp=index
                if heap.array[2*index+1]>=heap.array[2*index+2]:
                 heap.array[index],heap.array[2*index+1]=heap.array[2*index+1],heap.array[index]
                 index=2*temp+1
                else:
                    heap.array[index],heap.array[2*index+2]=heap.array[2*index+2],heap.array[index]
                    index=2*temp+2  
        @staticmethod            
         def heapify_process():
                for i in range(heap.heap_size,-1,-1):
                    heap.heapify(i)
         @staticmethod
         def get_max():
             max=heap.array[0]
             heap.array[0],heap.array[heap.heap_size-1]=heap.array[heap.heap_size-1],heap.array[0]
             heap.size--
             heap.array.pop()
             heap.heapify(0)
             return max
         @staticmethod
         def heap_insert(value):
             heap.array.append(value)
             heap.heap_size+=1
         @staticmethod
         def heap_clear():
             heap.array.clear()
             heap.heap_size=0
                
        

        
                
                        
                                        
   
     
       
         
           
                    