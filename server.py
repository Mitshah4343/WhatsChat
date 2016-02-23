#import pygtk
#pygtk.require('2.0')
import gtk, socket, select, thread, sys, helper, pango, gobject
from random import random
#gtk.gdk.threads_init()
gobject.threads_init()

def broadcast_data (sock, message):
	for socket in CONNECTION_LIST:
		if socket != server and socket != sock :
			try:
				socket.send(message)
			except :
				socket.close()
				CONNECTION_LIST.remove(socket)

def recv_msg(name):
	global CONNECTION_LIST, flag, server_obj, sock_name
	while not flag:
		read_sockets,write_sockets,error_sockets = select.select(CONNECTION_LIST,[],[])
		for sock in read_sockets:
			if sock == server:
				sockfd, addr = server.accept()
				data = sockfd.recv(4096)
				if data in sock_name.values():
					sockfd.send("@$__-_Change--name%$$$")
				else:
					CONNECTION_LIST.append(sockfd)
					sockfd.send(sock_name['<server>'] + "Welcome.....")
					sock_name[addr] = data
					server_obj.tags[str(addr)] = server_obj.textbuffer.create_tag(str(addr),foreground=gtk.gdk.Color(random()/2,random()/2,random()/2), weight=pango.WEIGHT_BOLD, right_margin=50)
					enditer = server_obj.textbuffer.get_end_iter()
					server_obj.textbuffer.insert(enditer, "%s entered room" % sock_name[addr] + '\n')
					adj = server_obj.sw.get_vadjustment()
					adj.set_value( adj.upper - adj.page_size )
					broadcast_data(sockfd, "%s entered room" % sock_name[addr])
			else:
				try:
					data = sock.recv(4096)
					addr = sock.getpeername()
					if data=="@$__-_fa--lse%$$$.":
						broadcast_data(sock, "%s is offline" % sock_name[addr])
						enditer = server_obj.textbuffer.get_end_iter()
						server_obj.textbuffer.insert(enditer, "%s is offline" % sock_name[addr] + '\n')
						adj = server_obj.sw.get_vadjustment()
						adj.set_value( adj.upper - adj.page_size )
						del sock_name[addr]
						sock.close()
						CONNECTION_LIST.remove(sock)
					else:
						broadcast_data(sock, '%s : '%sock_name[addr] + data)
						enditer = server_obj.textbuffer.get_end_iter()
						server_obj.textbuffer.insert_with_tags(enditer, '%s '%sock_name[addr], server_obj.tags[str(addr)])
						enditer = server_obj.textbuffer.get_end_iter()
						server_obj.textbuffer.insert(enditer, ': '+ data + '\n')
						adj = server_obj.sw.get_vadjustment()
						adj.set_value( adj.upper - adj.page_size )
				except:
					broadcast_data(sock, "%s is offline" % sock_name[addr])
					enditer = server_obj.textbuffer.get_end_iter()
					server_obj.textbuffer.insert(enditer, "%s is offline" % sock_name[addr] + '\n')
					adj = server_obj.sw.get_vadjustment()
					adj.set_value( adj.upper - adj.page_size )
					sock.close()
					CONNECTION_LIST.remove(sock)


# Class for GUI
class st:
	def exit(*args):
		broadcast_data(server, "@$__-_fa--lse%$$$")
		gtk.main_quit()
		server.close()
	
	def send(self, widget):
		txt = self.entry.get_text()
		self.entry.set_text('')
		if txt=='':
			return
		broadcast_data(server, sock_name['<server>']+txt)
		enditer = self.textbuffer.get_end_iter()
		self.textbuffer.insert_with_tags(enditer, txt + '\n', self.tag1)
		adj = self.sw.get_vadjustment()
		adj.set_value( adj.upper - adj.page_size - 1)
	
	def __init__(self):
		self.tags = {}
		self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
		self.window.set_resizable(True)
		self.window.set_default_size(300, 360)
		self.window.set_title("WhatChat")
		self.window.set_border_width(10)
		self.window.connect("destroy", self.exit)
		self.window.connect("delete_event", self.exit)
		box2 = gtk.VBox(False, 0)
		box1 = gtk.VBox(False, 0)
		box1.set_border_width(10)
		box2.pack_start(box1, True, True, 0)
		
		self.sw = gtk.ScrolledWindow()
		self.sw.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)
		#self.sw.set_placement(gtk.CORNER_BOTTOM_LEFT)
		self.textview = gtk.TextView()
		self.textview.modify_base(gtk.STATE_NORMAL, gtk.gdk.Color(0.99, 0.94, 0.96))
		self.textview.set_editable(False)
		self.textview.set_cursor_visible(False)
		self.textview.set_wrap_mode(gtk.WRAP_WORD_CHAR)
		self.textbuffer = self.textview.get_buffer()
		#self.tag1 = self.textbuffer.create_tag('tag1', foreground = gtk.gdk.Color(0.0, 0.2, 0.8))
		self.tag1 = self.textbuffer.create_tag('tag1', justification = gtk.JUSTIFY_RIGHT, style=pango.STYLE_ITALIC, left_margin=50)
		#self.tag1.set_left_margin(10)
		self.sw.add(self.textview)
		box1.pack_start(self.sw)
		
		separator = gtk.HSeparator()
		box1.pack_start(separator, False, True, 0)
		
		self.entry = gtk.Entry(max=0)
		self.entry.connect('activate', self.send)
		box1.pack_start(self.entry, False, False, 0)
		
		separator2 = gtk.HSeparator()
		box1.pack_start(separator2, False, True, 0)
		
		h1 = gtk.HBox(False, 0)
		h1.set_border_width(10)
		
		b1 = gtk.Button("Send")
		b1.connect("clicked", self.send)
		h1.pack_start(b1, True, True, 0)
		b2 = gtk.Button("Exit")
		b2.connect("clicked", self.exit)
		h1.pack_start(b2, True, True, 0)
		box2.pack_start(h1, False, False, 0)
		
		self.window.add(box2)
		self.window.show_all()

	def main(self):
		thread.start_new_thread (recv_msg, ("Thread-1", ))
		gtk.main()


if __name__ == "__main__":

	name = ''
	while name=='':
		name = helper.get_name()
	if name==False:
		sys.exit()
	
	
	host, port = helper.get_connection_details()
	while host=='' or port=='':
		host, port = helper.get_connection_details()
	if host==False and port==False:
		sys.exit()
	
	sock_name = {}
	sock_name['<server>'] = name + ' : '
	sock_name[name] = name
	CONNECTION_LIST = []
	flag = 0
	server = socket.socket()
	
	try:
		server.bind((host, int(port)))
	except:
		helper.errMsg()
		sys.exit()
	server.listen(10)
	CONNECTION_LIST.append(server)
	server_obj = st()
	server_obj.textbuffer.insert_at_cursor("Chat server started on port " + str(port) + '\n')
	server_obj.main()

