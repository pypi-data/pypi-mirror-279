def delete_all_files(directory=".", type={}):
    import os
    for filename in os.listdir(directory):
        for index, type in type.items():
            if filename.endswith((type)):
                filepath = os.path.join(directory, filename)
                try:
                    os.remove(filepath)
                    return f"Deleted: {filepath}"
                except OSError as e:
                    print (f"Error deleting {filepath}: {e}")
                    return f"Error deleting {filepath}: {e}"