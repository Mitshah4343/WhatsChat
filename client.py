import gtk, socket, select, thread, sys, helper, pango, gobject
from random import random
gobject.threads_init()

def send_msg(text):
	serv.send(text)

def recv_msg(name):
	global msg, flag, client_obj
	while not flag:
		socket_list = [sys.stdin, serv] 
		read_sockets,write_sockets,error_sockets = select.select(socket_list,[],[])
		for sock in read_sockets:
			if sock==serv:
				try:
					data = serv.recv(4096)
					if data=="@$__-_Change--name%$$$":
						flag=1
						helper.errName()
						gtk.main_quit()
					elif data=="@$__-_fa--lse%$$$":
						enditer = client_obj.textbuffer.get_end_iter()
						client_obj.textbuffer.insert(enditer, 'Disconnected from chat server' + '\n')
						adj = client_obj.sw.get_vadjustment()
						if adj!=None:
							adj.set_value(adj.upper - adj.page_size - 1)
						flag=1
					else:
						ind = data.find(':')
						if ind==-1:
							enditer = client_obj.textbuffer.get_end_iter()
							client_obj.textbuffer.insert(enditer, data + '\n')
							adj = client_obj.sw.get_vadjustment()
							if adj!=None:
								adj.set_value(adj.upper - adj.page_size - 1)
						else:
							name = data[:ind]
							if client_obj.tags.has_key(name)==False:
								client_obj.tags[name]=client_obj.textbuffer.create_tag(name,foreground=gtk.gdk.Color(random()/2,random()/2,random()/2), weight=pango.WEIGHT_BOLD, right_margin=50)
							enditer = client_obj.textbuffer.get_end_iter()
							client_obj.textbuffer.insert_with_tags(enditer, '%s'%name, client_obj.tags[name])
							enditer = client_obj.textbuffer.get_end_iter()
							client_obj.textbuffer.insert(enditer, data[ind:] + '\n')
							adj = client_obj.sw.get_vadjustment()
							adj.set_value( adj.upper - adj.page_size - 1)
				except:
					enditer = client_obj.textbuffer.get_end_iter()
					client_obj.textbuffer.insert(enditer, 'Disconnected from chat server' + '\n')
					adj = client_obj.sw.get_vadjustment()
					if adj!=None:
						adj.set_value(adj.upper - adj.page_size - 1)
					flag=1
						
# Class for GUI
class client:

	def exit(*args):
		send_msg("@$__-_fa--lse%$$$.")
		gtk.main_quit()
		sys.exit()
	
	def send(self, widget):
		global flag
		txt = self.entry.get_text()
		self.entry.set_text('')
		if txt=='':
			return
		enditer = self.textbuffer.get_end_iter()
		self.textbuffer.insert_with_tags(enditer, txt + '\n', self.tag1)
		adj = self.sw.get_vadjustment()
		if adj!=None:
			adj.set_value( adj.upper - adj.page_size - 1)
		if not flag:
			try:
				send_msg(txt)
			except:
				pass
	
	
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
		self.sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
		self.textview = gtk.TextView()
		self.textview.modify_base(gtk.STATE_NORMAL, gtk.gdk.Color(0.99, 0.94, 0.96))
		self.textview.set_editable(False)
		self.textview.set_cursor_visible(False)
		self.textview.set_wrap_mode(gtk.WRAP_WORD_CHAR)
		self.textbuffer = self.textview.get_buffer()
		self.tag1 = self.textbuffer.create_tag('tag1', justification = gtk.JUSTIFY_RIGHT, style=pango.STYLE_ITALIC)
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
	flag = 0
	
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
	
	serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	serv.settimeout(2)
	try :
		serv.connect((host, int(port)))
	except:
		helper.err()
		print "Unable to connect"
		sys.exit()
	
	send_msg(name)
	client_obj = client()
	client_obj.textbuffer.insert_at_cursor('Connected to remote host.' + '\n')
	client_obj.main()
