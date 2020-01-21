import random as rd

class update_file:

    def __init__(self):
        self.name = 'data.txt'
        self.index = 0
        self.size_plot = 40

    def data(self):
        read_file = open(self.name,'r').read()
        lines = read_file.split('\n')

        if len(lines)> self.size_plot:

            lines.pop(0)
            lines = lines 
            print(lines)
            with open(self.name,'w+') as update_file:
                for l in range(1,self.size_plot):
                    update_file.write('\n'+str(lines[l]))
            update_file.close()
            
    def update(self, index , sumvalue):
        self.data()
        with open(self.name,'a') as update_file:
            update_file.write('\n'+str(index)+','+(str(sumvalue)))
        update_file.close()
        
    def reset(self):
        f = open(self.name, 'w+')
        f.write('')
        f.close