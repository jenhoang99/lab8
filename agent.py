#!/usr/bin/env python3
import subprocess
import asyncio 

HOST = '127.0.0.1'
PORT = 12345

COMMAND_FILE = 'commands.conf'
KEY_INDEX = 0
COMMAND_INDEX = 1
  
def generate_command_list():
    '''
    Purpose: Generate a dictionary of commands from COMMAND_FILE
    Params: none
    Return: (list) a list of command from a text file
    Note:
        COMMAND_FILE contains a list of commands, 
        each command has command keys, commands and arguments, that are seperated by tabs
        => The function will split each command into a list to get the key for dictionary,
        the value for this key will the rest elements of this list
    '''
    command_list = {}
    try:
        with open(COMMAND_FILE, 'r') as f:
            lines = f.readlines()
            for command in lines:
                element_list = command.split()
                key = element_list[KEY_INDEX]
                command_list[key] = ' '.join(element_list[COMMAND_INDEX:])

    except Exception as e:    
        print(e)
    return command_list


def run_command(command):
    '''
    Purpose: Receive a text of command, excecute this command
    Params: (string) a text of command to execute
    Return (string) result of the command execution
    '''
    exec_command = command.split()
    return subprocess.check_output(exec_command, encoding='utf-8')


async def echo(reader, writer):
    '''
    Purpose: Run the main logic of agent that is called by asyncio.start_server
        * Receive request from manager (client)
        * Print request on the Terminal
        * Get the command based on the request message
        * Excecute the command
        * Send the result from the command execution
    Params:
        reader: An asyncio reader connected to the manager
        writer: An asyncio writer connected to the manager
    Return/Side Effects:
        The requested command will be executed on the server system
        If requested command won't be executed if not found in the command_list dictionary
    Note:
        If command is invalid, 'Invalid command' msg will be sent
        If it has any error during running the main logic, exception will be catched
            and 'Unexpected error' will be sent
    '''
    try:
        msg = await reader.readline()
        msg = msg.decode('utf-8').strip()
        print('Requested command about: ' + msg)
        command_list = generate_command_list()
        command = command_list.get(msg)
        if(command):
            output = run_command(command)
            writer.write(output.encode('utf-8'))
            await writer.drain()
        else:
            writer.write(b'Invalid command')
            await writer.drain()

    except Exception as e:
        print(e)
        writer.write(b'Unexpected error')
        await writer.drain()
    finally:
        writer.close()
        await writer.wait_closed()


async def main():
    '''
    Purpose: starts the agent server
    Params: N/A
    Return: N/A
    Notes: 
        Agent server run forever
    '''
    server = await asyncio.start_server(echo, HOST, PORT)
    await server.serve_forever() # make sure program  will not terminates

asyncio.run(main()) 

