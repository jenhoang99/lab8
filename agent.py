#!/usr/bin/env python3

HOST = '127.0.0.1'
PORT = 12345

command_file = 'commands.conf'


async def echo(reader, writer):
    try:
        
    except Exception as e:
        print(e)
    finally:
        writer.close()
        await writer.wait_closed()

async def main():
    server = await asyncio.start_server(echo, HOST, PORT)
    await server.serve_forever() # without this, program terminates

asyncio.run(main()) 