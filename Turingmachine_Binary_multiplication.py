import time
import copy
class Complex_TuringMachine_calculate_the_Y_power_of_X():
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.start_len=self.x+self.y+3#开始时纸带的长度
        self.start_state=('qs','l0','m0','n0')#初态
        self.final_state={('qf','l1','m1','n1'),('qf_1','l0','m0','n0'),('qf_2','l0','m0','n0'),('qf_3','l0','m0','n0')}#终态集合，qf_1代表碰到0乘0次的情况，qf_2代表碰到x（>=1）乘0，qf_3代表碰到0乘y（y>=1）
    def read_table(self):#从状态转移函数表中读取状态转移函数并放入字典中
        self.table_dic = {}
        with open('table3.txt', 'r',encoding='utf-8') as f:
            data = f.read().splitlines()#分行读取数据
            for line in data:
                if line:
                    tem=line.split(' ')
                    self.table_dic.update({((tem[0],tem[1],tem[2],tem[3]),tem[4],tem[5],tem[6],tem[7]):((tem[8],tem[9],tem[10],tem[11]),tem[12],tem[13],tem[14],tem[15],tem[16],tem[17],tem[18],tem[19])})#把转移函数放到字典中
        '''
        把x用0或者1替换
        '''
        dic_tem=copy.deepcopy(self.table_dic)
        for key in dic_tem.keys():
            if key[1]=='x':
                self.table_dic.update({(key[0],'1',key[2],key[3],key[4]):(self.table_dic[key][0],'1',self.table_dic[key][2],self.table_dic[key][3],self.table_dic[key][4],self.table_dic[key][5],self.table_dic[key][6],self.table_dic[key][7],self.table_dic[key][8])})
                self.table_dic.update({(key[0], '0', key[2], key[3], key[4]): (
                self.table_dic[key][0], '0', self.table_dic[key][2], self.table_dic[key][3], self.table_dic[key][4],
                self.table_dic[key][5], self.table_dic[key][6], self.table_dic[key][7], self.table_dic[key][8])})
                del self.table_dic[key]
        dic_tem=copy.deepcopy(self.table_dic)
        for key in dic_tem.keys():
            if key[2] == 'x':
                self.table_dic.update({(key[0], key[1], '1', key[3], key[4]): (
                self.table_dic[key][0], self.table_dic[key][1], '1', self.table_dic[key][3], self.table_dic[key][4],
                self.table_dic[key][5], self.table_dic[key][6], self.table_dic[key][7], self.table_dic[key][8])})
                self.table_dic.update({(key[0], key[1], '0', key[3], key[4]): (
                    self.table_dic[key][0], self.table_dic[key][1], '0', self.table_dic[key][3], self.table_dic[key][4],
                    self.table_dic[key][5], self.table_dic[key][6], self.table_dic[key][7], self.table_dic[key][8])})
                del self.table_dic[key]
        dic_tem = copy.deepcopy(self.table_dic)
        for key in dic_tem.keys():
            if key[3]=='x':
                self.table_dic.update({(key[0],key[1],key[2],'1',key[4]):(self.table_dic[key][0],self.table_dic[key][1],self.table_dic[key][2],'1',self.table_dic[key][4],self.table_dic[key][5],self.table_dic[key][6],self.table_dic[key][7],self.table_dic[key][8])})
                self.table_dic.update({(key[0], key[1], key[2], '0', key[4]): (
                self.table_dic[key][0], self.table_dic[key][1], self.table_dic[key][2], '0', self.table_dic[key][4],
                self.table_dic[key][5], self.table_dic[key][6], self.table_dic[key][7], self.table_dic[key][8])})
                del self.table_dic[key]
        dic_tem = copy.deepcopy(self.table_dic)
        for key in dic_tem.keys():
            if key[4]=='x':
                self.table_dic.update({(key[0],key[1],key[2],key[3],'1'):(self.table_dic[key][0],self.table_dic[key][1],self.table_dic[key][2],self.table_dic[key][3],'1',self.table_dic[key][5],self.table_dic[key][6],self.table_dic[key][7],self.table_dic[key][8])})
                self.table_dic.update({(key[0], key[1], key[2], key[3], '0'): (
                self.table_dic[key][0], self.table_dic[key][1], self.table_dic[key][2], self.table_dic[key][3], '0',
                self.table_dic[key][5], self.table_dic[key][6], self.table_dic[key][7], self.table_dic[key][8])})
                del self.table_dic[key]
    def init_tape(self):
        # 初始化纸带
        self.exponential_tape=['☐']+list(bin(self.x).replace('0b','')[::-1])+['☐']
        self.base_tape=['☐']+list(bin(self.y).replace('0b','')[::-1])+['☐']
        self.result_tape=['☐','0','☐']
        self.carry_tape=['☐','0','☐']
        # 初始化读头位置
        self.head_q=1
        self.head_l = 1
        self.head_m = 1
        self.head_n = 1
    def run(self):#图灵机运行
        transfer_time=0#记录状态转移次数
        start_time=time.time()
        self.init_tape()
        self.read_table()
        state=self.start_state#置状态为初始状态


        self.show_tape_and_head(state)#展示纸带和读头位置


        while state not in self.final_state:#如果状态没有到达终态，继续进行状态转移
            if (state,self.exponential_tape[self.head_q],self.base_tape[self.head_l],self.result_tape[self.head_m],self.carry_tape[self.head_n]) in self.table_dic.keys():#如果能在转移函数字典中找到当前状态对应的转移函数
                '''
                状态转移，读写纸带
                '''
                transfer_time+=1
                tem2=self.table_dic[(state,self.exponential_tape[self.head_q],self.base_tape[self.head_l],self.result_tape[self.head_m],self.carry_tape[self.head_n])]
                print('\033[1;32m↓ δ(' + state[0]+ ','+state[1]+ ','+state[2]+ ','+state[3]+ ','+self.exponential_tape[self.head_q]+','+self.base_tape[self.head_l]+','+self.result_tape[self.head_m]+','+self.carry_tape[self.head_n] + ') =', '('+tem2[0][0]+','+tem2[0][1]+','+tem2[0][2]+','+tem2[0][3]+','+tem2[1]+','+tem2[2]+','+tem2[3]+','+tem2[4]+','+tem2[5]+','+tem2[6]+','+tem2[7]+','+tem2[8]+')')#输出当前使用的转移函数
                state=tem2[0]
                self.exponential_tape[self.head_q]=tem2[1]
                self.base_tape[self.head_l]=tem2[2]
                self.result_tape[self.head_m]=tem2[3]
                self.carry_tape[self.head_n]=tem2[4]


                if tem2[5]=='L':
                    self.head_q-=1
                elif tem2[5]=='R':
                    self.head_q+=1
                elif tem2[5]=='S':
                    pass
                else:
                    print('\033[3;31mWarning : Moving direction is wrong!')#如果转移方向不为L,R或者S
                    break


                if tem2[6] == 'L':
                    self.head_l -= 1
                    if self.head_l==0:
                        self.base_tape.insert(0,'☐')# 如果读头位置超出了当前纸带长度，动态延长纸带
                        self.head_l+=1
                elif tem2[6] == 'R':
                    self.head_l += 1
                elif tem2[6] == 'S':
                    pass
                else:
                    print('\033[3;31mWarning : Moving direction is wrong!')  # 如果转移方向不为L,R或者S
                    break


                if tem2[7] == 'L':
                    self.head_m -= 1
                elif tem2[7] == 'R':
                    self.head_m += 1
                    if self.head_m>=len(self.result_tape):#如果读头位置超出了当前纸带长度，动态延长纸带
                        self.result_tape.append('☐')
                elif tem2[7] == 'S':
                    pass
                else:
                    print('\033[3;31mWarning : Moving direction is wrong!')  # 如果转移方向不为L,R或者S
                    break


                if tem2[8] == 'L':
                    self.head_n -= 1
                elif tem2[8] == 'R':
                    self.head_n += 1
                elif tem2[8] == 'S':
                    pass
                else:
                    print('\033[3;31mWarning : Moving direction is wrong!')  # 如果转移方向不为L,R或者S
                    break

                self.show_tape_and_head(state)#展示本次转移后的纸带
            else:
                print('\033[3;31mWarning : Can\'t find transfer function!')#如果找不到当前状态对应的转移函数
                break
        final_time = time.time()
        if state in self.final_state:
            if state==('qf','l1','m1','n1'):#正整数乘正整数
                print('\033[1;35m计算结果为：', int(''.join(self.result_tape).replace('☐', '')[::-1], 2))  # 计算结果
                print('所用时间：', final_time - start_time)
                print('状态转移次数为：', transfer_time)
            else:#结果为零的情况
                print('\033[3;35m计算结果为：', 0)
                print('所用时间：', final_time - start_time)
                print('状态转移次数为：', transfer_time)
    def show_tape_and_head(self,state):#可视化展示纸带和读头位置的方法
        tape_q=self.exponential_tape
        tape_l=self.base_tape
        tape_m =self.result_tape
        tape_n = self.carry_tape
        print('\033[1;33m┌————' + '┬————' * (len(tape_q)-1) + '┐')
        for t in range(len(tape_q)):
            if tape_q[t]=='☐':
                print('| ' + ' ' + '  ', end='')
            else:
                print('| ' + tape_q[t] + '  ', end='')
        print('|' )
        print('└————' + '┴————' * (len(tape_q)-1) + '┘')
        print('     ' * self.head_q + '   ↑')
        print('     ' * self.head_q + '┌————┐' )
        print('     ' * self.head_q + '|' + state[0] + ' '*(-len(state[0])+4)+'|')
        print('     ' * self.head_q + '└————┘')

        print('\033[1;33m┌————' + '┬————' * (len(tape_l) - 1) + '┐')
        for t in range(len(tape_l)):
            if tape_l[t]=='☐':
                print('| ' + ' ' + '  ', end='')
            else:
                print('| ' + tape_l[t] + '  ', end='')
        print('|')
        print('└————' + '┴————' * (len(tape_l) - 1) + '┘')
        print('     ' * self.head_l + '   ↑')
        print('     ' * self.head_l + '┌————┐')
        print('     ' * self.head_l + '|' + state[1] + ' ' * (-len(state[1]) + 4) + '|')
        print('     ' * self.head_l + '└————┘')

        print('\033[1;33m┌————' + '┬————' * (len(tape_m) - 1) + '┐')
        for t in range(len(tape_m)):
            if tape_m[t]=='☐':
                print('| ' + ' ' + '  ', end='')
            else:
                print('| ' + tape_m[t] + '  ', end='')
        print('|')
        print('└————' + '┴————' * (len(tape_m) - 1) + '┘')
        print('     ' * self.head_m + '   ↑')
        print('     ' * self.head_m + '┌————┐')
        print('     ' * self.head_m + '|' + state[2] + ' ' * (-len(state[2]) + 4) + '|')
        print('     ' * self.head_m + '└————┘')

        print('\033[1;33m┌————' + '┬————' * (len(tape_n) - 1) + '┐')
        for t in range(len(tape_n)):
            if tape_n[t]=='☐':
                print('| ' + ' ' + '  ', end='')
            else:
                print('| ' + tape_n[t] + '  ', end='')
        print('|')
        print('└————' + '┴————' * (len(tape_n) - 1) + '┘')
        print('     ' * self.head_n + '   ↑')
        print('     ' * self.head_n + '┌————┐')
        print('     ' * self.head_n + '|' + state[3] + ' ' * (-len(state[3]) + 4) + '|')
        print('     ' * self.head_n + '└————┘')

        print('\033[1;36m=======================================================================')
if __name__=='__main__':
    aa=Complex_TuringMachine_calculate_the_Y_power_of_X(5,2)
    aa.run()
