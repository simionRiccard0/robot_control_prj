## UR communication module

import socket
import struct, time, threading
import ast
import queue
import cfg

def tcp_init():
	print((cfg.ip_address, cfg.trgt_port))
	cfg.snd_q = queue.Queue()
	cfg.rcv_q = queue.Queue()
	cfg.thread_list = []
	cfg.comm_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	cfg.comm_socket.bind((cfg.ip_address, cfg.trgt_port))
	cfg.comm_socket.settimeout(10)
	cfg.comm_socket.listen()
	#cfg.comm_socket = s

def sock_init():
	try:
		cfg.host, cfg.port = cfg.comm_socket.accept()
		print("Connected to socket "+str(cfg.host))
	except Exception as e:
		print(e)

def safe_eval(expression):
	try:
		result = ast.literal_eval(expression)
		return result
	except (ValueError, SyntaxError) as e:
		return f"Error: {e}"

def send_data(data):
	if data is not None and cfg.snd_q is not None:
		try:
			cfg.snd_q.put(data, timeout = 1)
		except cfg.snd_q.timeout:
			print("Data Queue failed")

def recv_data():
	if cfg.rcv_q is not None and not(cfg.rcv_q.empty()):
		data = cfg.rcv_q.get(False)
	else:
		data = None
	return data


def send_lp(host, port):
	while True :
		if not(cfg.snd_q.empty()):
			for i in range(cfg.snd_q.qsize()):
				try:
					data = cfg.snd_q.get() #One element at the time
					tmp_cnt = str(data) #Quick & dirty string conversion
					binStr = tmp_cnt.encode('ascii')
					host.sendall(binStr)
				except Exception as e:
					print(e)
		else:
			time.sleep(0.1)


def recv_lp(host, port):
	rec_arr = None
	while True:
		try:
			tmp_recv = host.recv(1024)
			if not data:
				break  # Connection closed
			try:
				tmp_data = tmp_recv.decode('ascii')
				cfg.rcv_q.put(safe_eval(tmp_data))
			except Exception as e_str:
				print(e_str)
		except socket.timeout:
			# No data received within the timeout period
			continue
		except Exception as e:
			print(e)
			break

def ur_client():
	pass

