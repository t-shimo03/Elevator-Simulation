import matplotlib.pyplot as plt
from matplotlib import animation as anim
import random
import tkinter as tk
import tkinter.ttk as ttk
import matplotlib.patches as patches
import numpy as np

sim_app = tk.Tk()
sim_app.geometry("500x300")
sim_app.title("Escalator-Simulation")
sim_step = 0

var_scale = tk.IntVar(value=0)
def label_view(self):
    l["text"] = "Percentage of Walking : " + str(var_scale.get()) + "%"
l = tk.Label(
    sim_app,
    text= "Percentage of Walking : " + str(var_scale.get()) + "%",
    )
l.place(x = 10, y = 10)
scale = ttk.Scale(sim_app,length = 100, from_=0, to=100,
                  orient=tk.HORIZONTAL,variable=var_scale,command=label_view)
scale.place(x = 300, y = 10)

l_mode = tk.Label(
    sim_app,
    text= "Simulation Mode :",
    )
l_mode.place(x =10, y = 60)

v = tk.StringVar()
combobox = ttk.Combobox(sim_app, height=3, textvariable= v, state="readonly", values=('Walker', 'Stop'))
combobox.place(x = 200,y = 60)

l_user = tk.Label(
    sim_app,
    text= "Total People : 300",
    )
l_user.place(x =10, y = 110)
l_step = tk.Label(
    sim_app,
    text= "Simulation Step : " + str(sim_step),
    )
l_step.place(x =10, y = 160)

def main_sim():
    right_list = []
    left_list = []
    right_x = []
    left_x = []
    img_list = []
    mode = combobox.get()

    fig = plt.figure()
    ax = fig.subplots()
    plt.xlim(-25,25)
    plt.ylim(-50,120)
    r = patches.Rectangle(xy=(-5, 0), width=10, height=80, ec='#000000', fc = '#808080')
    ax.add_patch(r)
    #全体の人数
    user = 300

    #歩行者の割合
    walker = var_scale.get()
    if mode == "Stop":
        walker = 50
    if walker == 0:
        walker = 50

    #歩く人数
    left = int(user / 100 * walker)
    #立ち止まる人数
    right = user - left

    #歩行者の速度(m/s)
    v_w = 4

    #エスカレータの速度(m/s)
    v_e = 4
    for i in range(right):
        right_list.append((-4 * i))
        right_x.append(4)
    
    if mode == "Walker":
        for i in range(left):
            left_list.append((-4 * i) - random.choice(np.arange(0,2,1)))
            left_x.append(-4)
    if mode == "Stop":
        for i in range(left):
            left_list.append((-4 * i))
            left_x.append(-4)

    #シミュレーションのステップ数カウンター
    sim_step = 0
    img = plt.plot(10000,10000,color = 'red',linestyle='None', marker='.',label = "stop")
    if mode == "Walker":
        img += plt.plot(10000,10000,color = 'blue',linestyle='None', marker='.',label = "walker")
    if mode == "Stop":
        img += plt.plot(10000,10000,color = 'blue',linestyle='None', marker='.',label = "stop")

    img_list.append(img)
    while True:
        for i in range(right):
            if right_list[i] >= 0 and right_list[i] < 80:
                right_list[i] += v_e
            if right_list[i] < 0 and right_list[i] >= -4:
                right_list[i] += 2
            else:
                right_list[i] += v_w
        for i in range(left):
            if mode == "Walker":
                if left_list[i] >= 0 and left_list[i] < 80:
                    left_list[i] += v_e + v_w
                else:
                    left_list[i] += v_w
            
            if mode == "Stop":
                if left_list[i] >= 0 and left_list[i] < 80:
                    left_list[i] += v_e
                if left_list[i] < 0 and left_list[i] >= -4:
                    left_list[i] += 2
                else:
                    left_list[i] += v_w
        

        img = ax.plot(left_x,left_list,color = 'blue',linestyle='None', marker='.')
        img += ax.plot(right_x,right_list,color = 'red',linestyle='None', marker='.')
        img_list.append(img)
        sim_step += 1
        l_step = tk.Label(
        sim_app,
        text= "Simulation Step : " + str(sim_step),
        )
        l_step.place(x =10, y = 160) 
        if right_list[right -1] >= 80 and left_list[left -1] >= 80:
            break
    plt.legend()
    ani = anim.ArtistAnimation(fig, img_list, interval = 50)
    ani.save("result/result_" + mode + "_" + str(walker) + ".gif", writer="pillow")

    l_Saved = tk.Label(
    sim_app,
    text= "Saved result_" + mode + "_" + str(walker) + ".gif",
    )
    l_Saved.place(x =10, y = 210)
    plt.show()
    plt.close()

button1=tk.Button(sim_app,text="run simulation",width=20,command=main_sim)
button1.place(x=125,y=250)
sim_app.mainloop()