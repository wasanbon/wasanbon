import os, sys, json, traceback

import tornado.ioloop
import tornado.web
import tornado.websocket
from tornado.ioloop import PeriodicCallback

from tornado.options import define, options, parse_command_line


ws = None
idl_plugin = None

class IndexHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self):
        self.render("index.html")


class SendWebSocket(tornado.websocket.WebSocketHandler):
    #on_message -> receive data
    #write_message -> send data

    # called when connection established

    _handshake_message = 'wasanbon_converter'
    _handshake_response = 'wasanbon_converter ready'

    outports = {}
    _verbose = True

    def open(self):
        self._ready = False
        self._test = False
        if self._verbose: print " - WebSocket opened" 

    def check_origin(self, origin):
        return True

    def allow_draft76(self):
        return True

    def _on_handshake(self, message):
        tokens = message.split(' ')
        if not tokens[0] == self._handshake_message:
            print ' -- Error. Invalid message %s' % message
            return
        for t in tokens:
            if t.startswith('test='):
                print 'test is ', t
                self._test = t.split('=')[1][1:-1] == 'true'
                
            
        self.write_message(self._handshake_response)
        if self._verbose: ' -- HandShake Okay.'

        try:
            import rtcomponent
            comp = rtcomponent.component
            print comp.get_context(0).activate_component(comp.getObjRef())
        except:
            traceback.print_exc()

        self._ready = True
        global ws
        ws = self

        if self._test:
            self._start_test_mode()

    def on_message(self, message):
        if not self._ready:
            return self._on_handshake(message)
        else:
            self._on(message);

    def _on(self, message):
        if message.startswith('manager'):
            self._on_manager(message[len('manager')+1:])
        elif message.startswith('OutPort'):
            self._on_OutPort(message[len('OutPort')+1:])
        elif message.startswith('CorbaPort'):
            self._on_CorbaPort(message[len('CorbaPort')+1:])


    def _on_manager(self, message):
        if self._verbose: print 'manager message: ', message
        if message.startswith('addInPort'):
            if self._onAddInPort(message[len('addInPort')+1:]):
                print 'true'
                self.write_message('wsconverter addInPort true')
            else:
                self.write_message('wsconverter addInPort false')

        if message.startswith('addOutPort'):
            if self._onAddOutPort(message[len('addOutPort')+1:]):
                print 'true'
                self.write_message('wsconverter addOutPort true')
            else:
                self.write_message('wsconverter addOutPort false')

        if message.startswith('addCorbaPort'):
            if self._onAddCorbaPort(message[len('addCorbaPort')+1:]):
                print 'true'
                self.write_message('wsconverter addCorbaPort true')
            else:
                self.write_message('wsconverter addCorbaPort false')

        if message.startswith('removeAllPort'):
            if self._onRemoveAllPort():
                print 'true'
                self.write_message('wsconverter removeAllPort true')
            else:
                self.write_message('wsconverter removeAllPort false')

    def _on_CorbaPort(self, message):
        if self._verbose: print 'CorbaPort message: ', message
        if message.split(' ')[0] == 'invoke':
            val = self._on_CorbaPort_invoke(message[len('invoke')+1:].strip())
            self.write_message('wsconverter CorbaPort ' + val)

    def _on_CorbaPort_invoke(self, message):
        tokens = message.split(' ')
        portName = tokens[0]
        interfaceName = tokens[1]
        interfaceTypeName = tokens[2]
        methodName = tokens[3]

        value_str = message[ len(tokens[0]) + len(tokens[1]) + len(tokens[2]) + len(tokens[3]) + 3: ]
        d_ = json.loads(value_str)
        print 'invoke %s %s %s %s' % (interfaceName, interfaceTypeName, methodName, d_)
        #name = d_.keys()[0]
        #if not name in self.outports.keys():
        #    print '# Error. No OutPort (name=%s) is registerd.' % name
        #    return
        #self.outports[name](d_[name])
        import rtcomponent
        invoker_name = interfaceName + '_call_' + methodName
        invoker = getattr(rtcomponent.component.loaded_modules[portName + '_CorbaPort'], invoker_name)
        val = invoker(*d_)
        print 'retval=', val
        open('output', 'w').write(str(repr(val)))
        return json.dumps(val)

    def _on_OutPort(self, message):
        if self._verbose: print 'OutPort message: ', message
        d_ = json.loads(message.strip())
        name = d_.keys()[0]
        if not name in self.outports.keys():
            print '# Error. No OutPort (name=%s) is registerd.' % name
            return
        self.outports[name](d_[name])
            
    def _onRemoveAllPort(self):
        if self._verbose: print 'removeAllPort'
        import rtcomponent
        rtcomponent.component.removeAllPort()
        return True
        

    def _onAddInPort(self, message):
        name = message.split(' ')[0].strip()
        typename = message.split(' ')[1].strip()
        if self._verbose: print 'AddInPort', name, typename

        idl_plugin.parse()
        import inport_converter as ip
        verbose = True
        ip.create_inport_converter_module(idl_plugin.get_idl_parser(), name, typename, verbose=verbose)

        modulename = name.strip() + '_InPort_' + typename.replace('::', '_').strip()
        if self._verbose: print 'module:', modulename
        import rtcomponent
        rtcomponent.component.load(modulename)
        return True

    def _onAddOutPort(self, message):
        name = message.split(' ')[0].strip()
        typename = message.split(' ')[1].strip()
        if self._verbose: print 'AddOutPort', name, typename

        idl_plugin.parse()
        import outport_converter as op
        verbose = True
        op.create_outport_converter_module(idl_plugin.get_idl_parser(), name, typename, verbose=verbose)

        modulename = name.strip() + '_OutPort_' + typename.replace('::', '_').strip()
        if self._verbose: print 'module:', modulename
        import rtcomponent
        rtcomponent.component.load(modulename)
        return True

    def _onAddCorbaPort(self, message):
        name = message.split(' ')[0].strip()
        if self._verbose: print 'AddCorbaPort', name
        interface_names = message.split(' ')[1:]
        consumers = []
        providers = []
        for i in interface_names:
            if i.endswith('.consumer'):
                consumers.append(i[:-(len('.consumer'))])
            elif i.endswith('.provider'):
                providers.append(i[:-(len('.provider'))])
        
        idl_plugin.parse()
        import serviceport_converter as sp
        verbose = True
        sp.create_serviceport_converter_module(idl_plugin.get_idl_parser(), name, consumers, providers, verbose=verbose)

        modulename = name.strip() + '_CorbaPort'
        if self._verbose: print 'module:', modulename
        import rtcomponent
        rtcomponent.component.load(modulename)
        return True
        
    # on callback start
    def _send_message(self):
        
        self.i += 1
        self.write_message(str(self.i))

    # when connection disconnected.
    def on_close(self):
        #self.callback.stop()
        if self._verbose: print " - WebSocket closed"
        self._ready = False
        import rtcomponent
        try:
            comp = rtcomponent.component
            print comp.get_context(0).activate_component(comp.getObjRef())
        except:
            traceback.print_exc()
        


    def _start_test_mode(self):
        import RTC
        data = RTC.Time(0,0)
        test_msg = '''
'RTC::Time':
  sec: 0
  usec: 0
'''.strip()
        self.write_message(test_msg)
