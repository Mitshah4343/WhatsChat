import gtk

def errMsg():
	dialog = gtk.Dialog("",
		               None,
		               gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
		                (gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))
	
	dialog.set_geometry_hints(dialog, 400, 100, 400, 100)
	l1 = gtk.Label("Error :")
	dialog.vbox.pack_start(l1)
	l1.show()
	
	label = gtk.Label("Server can't be created on this host-address and port")
	dialog.vbox.pack_start(label)
	label.show()
	response = dialog.run()
	dialog.destroy()


def errName():
	dialog = gtk.Dialog("",
		               None,
		               gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
		                (gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))
	
	dialog.set_geometry_hints(dialog, 500, 100, 500, 100)
	l1 = gtk.Label("Error :")
	dialog.vbox.pack_start(l1)
	l1.show()
	label = gtk.Label("Nickname already taken. Please change your Nickname and try again")
	dialog.vbox.pack_start(label)
	label.show()
	response = dialog.run()
	dialog.destroy()

def err():
	dialog = gtk.Dialog("",
		               None,
		               gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
		                (gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))
	
	dialog.set_geometry_hints(dialog, 200, 100, 200, 100)
	l1 = gtk.Label("Error :")
	dialog.vbox.pack_start(l1)
	l1.show()
	label = gtk.Label("Unable to connect")
	dialog.vbox.pack_start(label)
	label.show()
	response = dialog.run()
	dialog.destroy()

def get_name():
	dialog = gtk.Dialog("",
		               None,
		               gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
		               (gtk.STOCK_OK, gtk.RESPONSE_ACCEPT,
		               gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT))

	label = gtk.Label("Nick Name:")
	dialog.vbox.pack_start(label)
	label.show()
	entry1 = gtk.Entry(max=0)
	dialog.vbox.pack_start(entry1)
	entry1.show()
	response = dialog.run()
	if response==-3:
		name = entry1.get_text()
	else:
		name = False
	dialog.destroy()
	return name
	
def get_connection_details():
	dialog = gtk.Dialog("",
		               None,
		               gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
		               (gtk.STOCK_OK, gtk.RESPONSE_ACCEPT,
		                gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT))

	h1 = gtk.HBox(False, 0)
	dialog.vbox.pack_start(h1)
	h1.show()
	h2 = gtk.HBox(False, 0)
	dialog.vbox.pack_start(h2)
	h2.show()
	label1 = gtk.Label("HOST: ")
	h1.pack_start(label1)
	label1.show()
	entry1 = gtk.Entry(max=0)
	entry1.set_text('127.0.0.1')
	h1.pack_start(entry1)
	entry1.show()
	label2 = gtk.Label("PORT: ")
	h2.pack_start(label2)
	label2.show()
	entry2 = gtk.Entry(max=0)
	entry2.set_text('2000')
	h2.pack_start(entry2)
	entry2.show()

	response = dialog.run()
	if response==-3:
		name = entry1.get_text()
		port = entry2.get_text()
	else:
		name = False
		port = False
	dialog.destroy()
	
	return (name, port)


if __name__=="__main__":
	errMsg()

