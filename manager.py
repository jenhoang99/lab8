#!/usr/bin/env python3
import asyncio
import sys

AGENTS_FILE = 'agents.conf'
BUF_SIZE = 1024

async def get_msg(reader):
    '''
    Purpose: receive the message from agent via reader and return that message
    Params:
        reader: An asyncio reader connected to the agent
    Return/Side Effect:
        receive_msg (byte) the message from agent via reader

    '''
    receive_msg = b''
    while True:                        
        next_data = await reader.read(n = BUF_SIZE)                        
        if not next_data:                        
            break                      
        receive_msg = receive_msg + next_data   
    return receive_msg


async def contact_agent(command_key, host, port):
    '''
    Purpose: * Contact a agent via host and port value 
             * Send command_key to agent
             * Receive result from agent and print on the terminal
    Params:
        command_key (string) the key of the command to execute
        host (agent) the IPv6 address of the agent to contact
        port (int) the port number of agent to contact 
    Note: As the message from agent my contains 
    '''
    reader, writer = await asyncio.open_connection(host, port)        
    try:        
        writer.write(command_key.encode('utf-8') + b'\n') 
        await writer.drain()  
        receive_msg = await get_msg(reader)

        agent_info = writer.get_extra_info('peername')
        print(f"Response from {agent_info}")
        print(receive_msg.decode('utf-8') + '\n')   

    except Exception as e:        
        print(e)      
          
    finally:        
        writer.close()      
        await writer.wait_closed()


async def run_manager(command_key):
    '''
    Purpose: Receive command key from user input, 
            * Get agent list from AGENTS_FILE
            * Contact to each agent in the agents 
            by calling contact_agent() function and pass the command key, agent'shost and agent's port to this function
    Params: command_key (string) message request will be sent to each agent from user input
    Note:  AGENTS_FILE contains a list of agent address with IPv6 address and port, 
            that are separated by a tab
        => the function will split each line to assign to host and port variable

    '''
    try:
        with open(AGENTS_FILE, 'r') as f:
            agent_list = f.readlines()
            for agent_addr in agent_list:
                [host, port] = agent_addr.split()
                await contact_agent(command_key, host, port )
    except Exception as e:    
        print(e)


while True:
    request_command = input('Enter a command: \n')
    if(request_command.strip() != ''):
        break

asyncio.run(run_manager(request_command))
