#!/usr/bin/env python3
import subprocess
import asyncio 

HOST = '127.0.0.1'
PORT = 12345


COMMAND_FILE = 'commands.conf'
  
def generate_command_list():
    result = []
    try:
        with open(COMMAND_FILE, 'r') as f:
            command_list = f.readlines()
            result = list(map(lambda command: ' '.join(command.split()), command_list))
            #gfprint(result) 

    except Exception as e:    
        print(e)
    return result

def is_valid_command(command):
    is_valid = False
    #print(generate_command_list())
    if command.strip() in generate_command_list():
        is_valid = True    
    #print(is_valid)
    return is_valid


def run_command(command):
    exec_command = command.split()
    return subprocess.check_output(exec_command, encoding='utf-8')


async def echo(reader, writer):
    try:
        command = await reader.readline()
        #print(command)
        command = command.decode('utf-8')
        if(is_valid_command(command)):
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
    server = await asyncio.start_server(echo, HOST, PORT)
    await server.serve_forever() # without this, program terminates

asyncio.run(main()) 

