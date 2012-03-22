import os.path
import tornado.ioloop
import tornado.web
from tornado.options import options

class MainHandler(tornado.web.RequestHandler):
    def write_error(self, status_code, **kwargs):
        import traceback
        if self.settings.get("debug") and "exc_info" in kwargs:
            exc_info = kwargs["exc_info"]
            trace_info = ''.join(["%s<br/>" % line for line in traceback.format_exception(*exc_info)])
            request_info = ''.join(["<strong>%s</strong>: %s<br/>" % (k, self.request.__dict__[k] ) for k in self.request.__dict__.keys()])
            error = exc_info[1]
            
            self.set_header('Content-Type', 'text/html')
            self.finish("""<html>
                             <title>%s</title>
                             <body>
                                <h2>Error</h2>
                                <p>%s</p>
                                <h2>Traceback</h2>
                                <p>%s</p>
                                <h2>Request Info</h2>
                                <p>%s</p>
                             </body>
                           </html>""" % (error, error, 
                                        trace_info, request_info))
        
    def get(self):
        storm_chasers = ["TIV 1", "TIV 2"]
        
        self.render("home.html", 
                    storm_chasers=storm_chasers)                   


handlers = [
    (r"/", MainHandler),
]

settings = dict(
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        debug=True,
)
               
application = tornado.web.Application(handlers, **settings)

if __name__ == "__main__":
    tornado.options.parse_command_line()
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()