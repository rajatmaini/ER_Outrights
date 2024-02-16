start_price=130.63
spacing=0.01
order_spacing=2
no_orders=10
order_dict={}
sum = 0
c_list = []
for i in range(0,no_orders):
    if((i%order_spacing)==0):
        order_dict[start_price]=5
    else:
        order_dict[start_price]=0
    start_price -= spacing
for i in order_dict.values():
    if(i!=0):
        sum+= i
        c_list.append(sum)
    else:
        c_list.append(0)
print(c_list)