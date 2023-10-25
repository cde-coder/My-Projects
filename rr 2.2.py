def example():
    process_table = {
        "A ": [1, 6, 'C'],
        "B ": [2, 8, 'C'],
        "C ": [1, 3, 'C'],
        "D ": [3, 7, 'C'],
        "E ": [30, 5, 'C'],
        "F ": [60, 2, 'C']
    }
    slice = 5
    represent(process_table, 'P')
    return process_table, slice

def i_p(i):
    try:
        x = int(i)
    except ValueError:
        x = float(i)
    return x

def user_input():
  process_table = {}
  slice = i_p(input("Enter the Time Slice : "))
  while True:
    process_data = input("Enter process data (Process_ID, arrival-time, burst-time) or 'done' to finish: ")
    if process_data == "done":
      break
    process_info = process_data.split()
    process_id = process_info[0]
    arrival_time = i_p(process_info[1])
    burst_time = i_p(process_info[2])
    process_table[process_id]=[arrival_time, burst_time,'C']
  print(process_table)
  return process_table,slice

def represent(x,y):
  if y == 'P':
    print("Process Table :-")
    print("+" + "---------------+" * 3)
    print("|   Process\t|  Arrival Time | Burst Time  |")
    print("+" + "---------------+" * 3)
    for process, details in x.items():
        arrival_time,burst_time,trash = details
        print("|   ", process, "\t|   \t", arrival_time, "\t|   \t", burst_time, "  \t|")
    print("+" + "---------------+" * 3)
  elif y=='G':
      print("\nGantt Chart:\n")
      print("+" + "-------+" * len(x))
      print("|", end="")
      for i in x:
          print(f"   {i[1]}  |", end="")
      print()
      print("+" + "-------+" * len(x))
      print("", end="")
      print
      s=0
      print("0".format(i[2]), end="\t")
      for item in x:
            if isinstance(item[2], float):
                print("{:.2f}".format(item[2]), end="\t")
            else:
                print(f"{item[2]}", end="\t")
      print()

def round_robin(x, slice):
    ready_queue = []
    temp = dict(sorted(x.items(), key=lambda item: item[1][0]))
    time = 0
    keys_list = list(temp.keys())
    keys_to_process = [keys_list.pop(0)]
    
    while keys_to_process or any(value[2] == 'C' for value in temp.values()):        
        p = keys_to_process.pop(0)
        process = temp[p]
        if process[0] > time:
            ready_queue.append((time, "//", process[0], 0))
            time = process[0]
        temp[p][2] = 'R'
        if process[1] <= slice:
            end_time = time + process[1]
            ready_queue.append((time, p, end_time, process[0]))
            time = end_time
            temp[p][2] = 'R'
            for key, value in temp.items():
                m, _, o = value
                if 'C' in value and m <= time and m >= process[0]:
                    temp[key][2] = 'R'
                    keys_to_process.append(key)
            temp[p] = [process[0], (process[1] - slice), 'R']
        else:
            end_time = time + slice
            ready_queue.append((time, p, end_time, process[0]))
            time = end_time
            for key, value in temp.items():
                m, _, o = value
                if 'C' in value and m <= time and m >= process[0]:
                    temp[key][2] = 'R'
                    keys_to_process.append(key)
            temp[p] = [process[0], (process[1] - slice), 'R']
            if (process[1] - slice) != 0:
                keys_to_process.append(p)
        if not keys_to_process:
            for key, value in temp.items():
                if 'C' in value:
                    keys_to_process.append(key)
    
    represent(ready_queue, 'G')
    return ready_queue

def calAvg(x,reff):
    WT = []
    TAT = []
    t = []
    t1 = []
    print("Process_Id  Turn-Around-Time  Wait-Time")
    for i in reversed(x):
        if i[1] == "//" or i[1] in t:
            continue
        else:
            t1.append(i)
        t.append(i[1])
    t1.sort(key = lambda x : x[3])
    for i in t1:
        _,key,end,_ = i
        print("  ",key,"       ",end,"-",reff[key][0],"=",end-reff[key][0],"     ",end-reff[key][0],"-",reff[key][1],"=",(end-reff[key][0])-reff[key][1])
        WT.append(end-reff[key][0])
        TAT.append((end-reff[key][0])-reff[key][1])
    temp=temp1=0
    for i,j in zip(WT,TAT):
        temp+=i
        temp1+=j
    print("Average Turn around Time : {:.2f} ms".format(temp/len(TAT)))
    print("Average Wait-Time : {:.2f} ms".format(temp1/len(TAT)))

if __name__ == "__main__":
    process_table, slice = example() if input("Enter 'e': ") == 'e' else user_input()
    gantt = round_robin(process_table.copy(), slice)
    calAvg(gantt,process_table)


"""For future debugging
https://tinyurl.com/4vkpfk75
"""