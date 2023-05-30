
not_text_based_mime_types = ['video', 'image','audio','model','font']
print(any("video/3gpp2" in type for type in not_text_based_mime_types))