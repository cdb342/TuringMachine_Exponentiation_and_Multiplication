import time
class Standard_TuringMachine_calculate_the_Y_power_of_X():
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.start_len=self.x+self.y+3#开始时纸带的长度
        self.start_state='q0'#初态
        self.final_state={'qf','qf_1','qf_2','qf_3'}#终态集合，qf_1代表碰到0的0次的情况，qf_2代表碰到x（>=1）的0次，qf_3代表碰到0的y（y>=1）次
    def read_table(self):#从状态转移函数表中读取状态转移函数并放入字典中
        self.table_dic = {}
        with open('table.txt', 'r',encoding='utf-8') as f:
            data = f.read().splitlines()#分行读取数据
            for line in data:
                if line:
                    tem=line.split(' ')
                    self.table_dic.update({(tem[0],tem[1]):(tem[2],tem[3],tem[4])})#把转移函数放到字典中
    def init_tape(self):
        self.tape=['☐']+['1']*self.y+['0']+['1']*self.x+['0']*2+['☐']#初始化纸带
        self.head=1#初始化读头位置
    def run(self):#图灵机运行
        transfer_time=0#记录状态转移次数
        start_time=time.time()
        self.init_tape()
        self.read_table()
        state=self.start_state#置状态为初始状态
        self.show_tape_and_head(state)#展示纸带和读头位置
        while state not in self.final_state:#如果状态没有到达终态，继续进行状态转移
            if (state,self.tape[self.head]) in self.table_dic.keys():#如果能在转移函数字典中找到当前状态对应的转移函数
                '''
                状态转移，读写纸带
                '''
                transfer_time+=1
                tem2=self.table_dic[(state,self.tape[self.head])]
                print('\033[1;32m↓ δ(' + state+ ','+self.tape[self.head] + ') =', '('+tem2[0]+','+tem2[1]+','+tem2[2]+')')#输出当前使用的转移函数
                state=tem2[0]
                self.tape[self.head]=tem2[1]
                if tem2[2]=='L':
                    self.head-=1
                elif tem2[2]=='R':
                    self.head+=1
                    if self.head>=len(self.tape):#如果读头位置超出了当前纸带长度，动态延长纸带
                        self.tape.append('☐')
                else:
                    print('\033[3;31mWarning : Moving direction is wrong!')#如果转移方向不为L或者R
                    break
                self.show_tape_and_head(state)#展示本次转移后的纸带
            else:
                print('\033[3;31mWarning : Can\'t find transfer function!')#如果找不到当前状态对应的转移函数
                break
        final_time = time.time()
        if state in self.final_state:
            if state=='qf_1':#0的0次
                print('\033[3;31mWarning :The 0 power of 0!')
                print('所用时间：', final_time - start_time)
                print('状态转移次数为：',transfer_time)
            elif state=='qf_2':#x的0次，x>=1
                print('\033[3;35m计算结果为：',1)
                print('所用时间：', final_time - start_time)
                print('状态转移次数为：', transfer_time)
            elif state=='qf_3':#0的y次，y>=1
                print('\033[3;35m计算结果为：',0)
                print('所用时间：', final_time - start_time)
                print('状态转移次数为：', transfer_time)
            else:
                result=[k for k in self.tape if k!='☐']
                print('\033[1;35m计算结果为：',len(result)-self.start_len)#计算结果为最后的纸带长度减去开始时的纸带长度
                print('所用时间：',final_time-start_time)
                print('状态转移次数为：', transfer_time)
    def show_tape_and_head(self,state):#可视化展示纸带和读头位置的方法
        tape=[k for k in self.tape if k!='☐']
        print('\033[1;33m┌————' + '┬————' * (len(tape)+1) + '┐')
        print('| ' + ' ' + '  ', end='')
        for t in range(len(tape)):
            print('| ' + tape[t] + '  ', end='')
        print('| ' + ' ' + '  |')
        print('└————' + '┴————' * (len(tape)+1) + '┘')
        print('     ' * self.head + '   ↑')
        print('     ' * self.head + '┌————┐' )
        print('     ' * self.head + '|' + state + ' '*(-len(state)+4)+'|')
        print('     ' * self.head + '└————┘')
if __name__=='__main__':
    aa=Standard_TuringMachine_calculate_the_Y_power_of_X(1,1)
    aa.run()