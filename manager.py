#!/usr/bin/env python3
import asyncio
import sys

PORT = 12345
AGENTS_FILE = 'agents.conf'
BUF_SIZE = 1024



async def contact_agent(host, command):
    reader, writer = await asyncio.open_connection(host, PORT)        
    try:        
        writer.write(command.encode('utf-8') + b'\n') 
        await writer.drain()  
        receive_msg = b''
        while True:                        
            next_data = await reader.read(n = BUF_SIZE)                        
            if not next_data:                        
                break                      
            receive_msg = receive_msg + next_data
        addr = writer.get_extra_info('peername')
        print(f"Response from {addr}")
        print(receive_msg.decode('utf-8') + '\n')   

    except Exception as e:        
        print(e)      
          
    finally:        
        writer.close()      
        await writer.wait_closed()

async def run_manager(command):
    print(f"Run command: {command}")
    try:
        with open(AGENTS_FILE, 'r') as f:
            agent_list = f.readlines()
            for agent_addr in agent_list:
                print(agent_addr)
                await contact_agent(agent_addr.strip(), command)
    except Exception as e:    
        print(e)


while True:
    request_command = input('Enter a command: \n')
    if(request_command.strip() != ''):
        break

asyncio.run(run_manager(request_command))
