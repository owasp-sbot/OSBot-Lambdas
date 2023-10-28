import sys
sys.path.append('/opt/python')          # this needs to be done since LWA loses the path to the layers


from osbot_utils.testing.Temp_Web_Server import Temp_Web_Server

kwargs      = { "host"       : '127.0.0.1' ,
                "port"       : 8080        ,
                "root_folder": '/'         }            # set the root folder of the temp python webserver to be the root of the lambda vm
temp_web_server = Temp_Web_Server(**kwargs)             # note: this can be browsed via a lambda url :)

def run():
    temp_web_server.start()                             # start the server in a new thread (which will be picked up by LWA (Lambda Web Adapter)
    return temp_web_server.server_port_open()

if __name__ == "__main__":
    run()                                               # to be triggered from run.sh