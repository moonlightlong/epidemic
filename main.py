#!/usr/bin/python
# -*- coding: utf-8 -*-


from epidemic import Epidemic
import numpy as np
import matplotlib.pyplot as plt
import json

def get_data(G, rate=0.4, p=0):
	# 设置有效感染速度
	G.set_effective_spread_rate(rate)
	# 设置应激参数
	G.set_stimulation_paramter(0.2, 0.1)

	g01 = G.copy()
	g10 = G.copy()
	# 感染随时间
	print u"获取感染随时间变化数据"
	ratio_time_nomal = g01.spread()
	ratio_time0 = g10.spread_stress()
	g10.reset_nodes()
	g000 = g10.copy()
	ratio_time1 = g10.spread_stress()

	# 设置ratio间隔
	space = 0.02
	rate = 0.0
	rate_list = []
	while rate < 1.0:
		rate_list.append(rate)
		rate += space

	# 感染随有效传播速度的变化  当p==0时才求出
	print u"获取感染随有效传播速率的变化数据"
	if p == 0:
		ratio_rate_nomal = []
		ratio_rate0 = []
		ratio_rate1 = []
		for i in rate_list:
			print u" 速率：", i
			G.set_effective_spread_rate(i)
			g000.set_effective_spread_rate(i)
			g001 = G.copy()
			g010 = G.copy()
			g011 = g000.copy()
			ratio_rate_nomal.append(g001.spread())
			ratio_rate0.append(g010.spread_stress())
			ratio_rate1.append(g011.spread_stress())
		ratio_rate_nomal = sum(np.array(ratio_rate_nomal).T) / len(rate_list)
		ratio_rate0 = sum(np.array(ratio_rate0).T) / len(rate_list)
		ratio_rate1 = sum(np.array(ratio_rate1).T) / len(rate_list)
	else:
		ratio_rate_nomal = [0.0]
		ratio_rate0 = [0.0]
		ratio_rate1 = [0.0]
	data = {'nomal_time': list(ratio_time_nomal), 'time0': list(ratio_time0), 'time1': list(ratio_time1),
			'nomal_rate': list(ratio_rate_nomal), 'rate0': list(ratio_rate0), 'rate1': list(ratio_rate1)}
	return data
	
# 画出数据视图
def show_data(ws_data, ba_data, rate=0.4):
	name = r'rate%0.1f_time' % rate
	path = r'.../img/'
	plt.subplot(1, 2, 1)
	time = len(ws_data.get('nomal_time'))
	x = range(time)
	plt.plot(x, ws_data.get('nomal_time'), 'g-.h', label='The epidemic spreading without stress response')
	plt.plot(x, ws_data.get('time0'), 'r:*', label='The epidemic spreading with stress response 0')
	plt.plot(x, ws_data.get('time1'), 'b:o', label='The epidemic spreading with stress response 1')
	plt.xlabel(r'Time')
	plt.ylabel(r'$\rho$')
	plt.xlim(0, time)
	plt.ylim(0.0, 0.45)
	plt.xticks(np.linspace(0, time, (time - 1) // 2 + 1))
	plt.yticks(np.linspace(0.0, 0.45, 10))
	plt.legend(loc='lower right') 
	plt.subplot(1, 2, 2)
	plt.plot(x, ba_data.get('nomal_time'), 'g-.h', label='The epidemic spreading without stress response')
	plt.plot(x, ba_data.get('time0'), 'r:*', label='The epidemic spreading with stress response 0')
	plt.plot(x, ba_data.get('time1'), 'b:o', label='The epidemic spreading with stress response 1')
	plt.xlabel(r'Time')
	plt.ylabel(r'$\rho$')
	plt.xlim(0, time)
	plt.ylim(0.0, 0.45)
	plt.xticks(np.linspace(0, time, (time - 1) // 2 + 1))
	plt.yticks(np.linspace(0.0, 0.45, 10))
	plt.legend(loc='lower right')
	plt.savefig(path + name + '.png', dpi=500)
	plt.show()

	name = r'rate'
	plt.subplot(2, 1, 1)
	l = len(ws_data.get('nomal_rate'))
	x = range(l)
	plt.plot(x, ws_data.get('nomal_rate'), 'g-.h', label='The epidemic spreading without stress response')
	plt.plot(x, ws_data.get('rate0'), 'r:*', label='The epidemic spreading with stress response 0')
	plt.plot(x, ws_data.get('rate1'), ':o', label='The epidemic spreading with stress response 1')
	plt.xlabel(r'$\lambda$')
	plt.ylabel(r'$\rho$')
	plt.xlim(0, l)
	plt.ylim(0.0, 0.6)
	plt.xticks(np.linspace(0.0, l, l / 5 + 1))
	plt.yticks(np.linspace(0.0, 0.6, 13))
	plt.legend(loc='lower right') 
	plt.subplot(2, 1, 2)
	plt.plot(x, ba_data.get('nomal_rate'), 'g-.h', label='The epidemic spreading without stress response')
	plt.plot(x, ba_data.get('rate0'), 'r:*', label='The epidemic spreading with stress response 0')
	plt.plot(x, ba_data.get('rate1'), 'b:o', label='The epidemic spreading with stress response 1')
	plt.xlabel(r'$\lambda$')
	plt.ylabel(r'$\rho$')
	plt.xlim(0, l)
	plt.ylim(0.0, 0.6)
	plt.xticks(np.linspace(0.0, l, l / 5 + 1))
	plt.yticks(np.linspace(0.0, 0.6, 13))
	plt.legend(loc='lower right')
	plt.savefig(path + name + '.png', dpi=500)
	plt.show()

if __name__ == '__main__':
	G = Epidemic()
	ws = G.copy()
	print u"创建WS"
	ws.create_WS()
	print u"获得WS数据，稍等。。。"
	ws_data = get_data(ws)
	ba = G.copy()
	print u"创建BA"
	ba.create_BA()
	print u"获得BA数据，稍等。。。"
	ba_data = get_data(ba)
	print u"显示数据"
	show_data(ws_data, ba_data)
	print u"保存数据"
	with open(r'.../data/spread_data.json', 'w+') as f:
		f.write(json.dumps(ws_data))
		f.write(json.dumps(ba_data))
