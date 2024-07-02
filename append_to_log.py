def log_message(log_file_path,message):
    with open(log_file_path, 'a') as file:
        file.write(message + '\n')

# Example usage
if __name__=="__main__":
    log_message('This is a log entry.', 'Logs/log.txt')