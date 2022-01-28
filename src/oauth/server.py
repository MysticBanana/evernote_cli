import SocketServer
import socket
import SimpleHTTPServer
from threading import Thread
from helper import exception
import enum

class CallbackHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    class CallbackError(exception.EvernoteException):
        class ErrorReason(enum.Enum):
            DEFAULT = 1

    @property
    def query(self):
        query = {}
        if "?" in self.path:
            query = self.parse_querystr(self.path[self.path.find("?") + 1:])
        return query

    def parse_querystr(self, s):
        d = {}
        for k, kv in SimpleHTTPServer.urlparse.parse_qs(s, True, strict_parsing=True).items():
            if len(kv) > 1:
                d[k] = kv
            else:
                d[k] = kv[0]
        return d

    def end_headers(self):
        self.headers_sent = True
        return SimpleHTTPServer.SimpleHTTPRequestHandler.end_headers(self)

    def __getattr__(self, k):
        """handle any other METHOD requests"""
        if k.startswith("do_"):
            return self.do
        else:
            raise AttributeError(k)

    def do_HEAD(self):
        # overwrite
        return self.do()

    def do_GET(self):
        # overwrite
        return self.do()

    def do(self):
        ret = None
        self.headers_sent = False

        # todo redo
        try:
            try:
                ret = self.server.callback(self)
            except KeyError:
                if not self.headers_sent:
                    self.server.logger.error("501 Unsupported method {}".format(self.command))
                    # self.send_error(501, "Unsupported method {}".format(self.command))
                return

        except Exception as e:
            if not self.headers_sent:
                self.server.logger.error("500 {} - {}".format(e.__class__.__name__, e))
                # self.send_error(500, "{} - {}".format(e.__class__.__name__, e))

        else:
            if ret is None or ret == "" or ret == 0:
                if not self.headers_sent:
                    # self.send_response(204)
                    self.end_headers()

            else:
                if not self.headers_sent:
                    # self.send_response(200)
                    self.end_headers()

                self.wfile.write(ret)


class BasicServer(SocketServer.TCPServer):
    thread = None
    callback = None

    # https://github.com/python/cpython/blob/2.7/Lib/BaseHTTPServer.py#L102

    allow_reuse_address = 1  # Seems to make sense in testing environment

    class ServerError(exception.EvernoteException):
        class ErrorReason(enum.Enum):
            DEFAULT = 1

    @property
    def url(self):
        return "http://{}:{}".format(self.server_name, self.server_port)

    def server_bind(self):
        """Override server_bind to store the server name."""
        SocketServer.TCPServer.server_bind(self)
        host, port = self.socket.getsockname()[:2]
        self.server_name = socket.getfqdn(host)
        self.server_port = port

    def __init__(self, callback, hostname="", port=0, RequestHandlerClass=CallbackHandler, logger=None):
        SocketServer.TCPServer.__init__(self, (hostname, port), RequestHandlerClass)
        self.callback = callback
        self.logger = logger

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()

    def start(self):
        # maybe catch exception from serve
        if self.thread is not None:
            if self.logger:
                self.logger.warning("thread already exists")
            return False

        self.logger.info("starting server...")
        self.thread = Thread(target=self.serve_forever)
        self.thread.daemon = True
        self.thread.start()

    def stop(self):
        if self.thread is not None:
            self.logger.info("stopping server")
            self.shutdown()
            self.thread = None
