junkfile= open(save_location+'junk_text.txt',"w+")
	junk_string="".join(junk)
	junkfile.write(junk+'\n')
	junkfile.close()