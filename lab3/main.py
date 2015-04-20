import os.path
import glob

import tornado.web
import tornado.httpserver
import tornado.ioloop
import tornado.options

from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)

class IndexHandler(tornado.web.RequestHandler):
	def show_item(self, suffix):
		itemdir = os.path.join(os.path.dirname(__file__), "statics\songs");
		itemlist = [];
		for item in glob.glob(itemdir + "\\*." + suffix):
			itemlist = os.path.split(item);
		return itemlist;

	def show_size(self, mp3list):
		itemlist = mp3list;
		sizelist = {};
		for item in itemlist:
			sizelist[item] = os.path.getsize(item);
		return sizelist;

	def get(self):
		mp3list = self.show_item("mp3");
		sizelist = self.show_size(mp3list);
		self.render("music.html", mp3list=mp3list, sizelist=sizelist);

if __name__ == "__main__":
	tornado.options.parse_command_line();
	app = tornado.web.Application(
		handlers=[(r"/", IndexHandler)],
		template_path=os.path.join(os.path.dirname(__file__), "templates"),
		static_path=os.path.join(os.path.dirname(__file__), "statics"),
		debug=True
	);
	http_server = tornado.httpserver.HTTPServer(app);
	http_server.listen(options.port);
	tornado.ioloop.IOLoop.instance().start();
