import socket
from bottle import WSGIRefServer
from wsgiref.simple_server import make_server
from wsgiref.simple_server import WSGIRequestHandler, WSGIServer

class WebServer(WSGIRefServer):
  def run(self, app):
    #
    class FixedHandler(WSGIRequestHandler):
      def address_string(self):
        return self.client_address[0]
      def log_request(*args, **kw):
        if not self.quiet:
          return WSGIRequestHandler.log_request(*args, **kw)
    #
    handler_cls = self.options.get('handler_class', FixedHandler)
    server_cls  = self.options.get('server_class', WSGIServer)
    #
    if ':' in self.host:
      if getattr(server_cls, 'address_family') == socket.AF_INET:
        class server_cls(server_cls):
          address_family = socket.AF_INET6
    #
    srv = make_server(self.host, self.port, app, server_cls, handler_cls)
    self.srv = srv
    srv.serve_forever()

  def shutdown(self):
    self.srv.shutdown()

# server = WebServer(host="0.0.0.0", port=self.settings('lport'))
# serv_thread = threading.Thread(target=runServer, args=(server,))
# serv_thread.name = 'Autogram:Bottle'
# serv_thread.daemon = True
# serv_thread.start()