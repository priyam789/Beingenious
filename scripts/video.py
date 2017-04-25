from base import *

class ServeVideo(blobstore_handlers.BlobstoreDownloadHandler):
	def get(self, blob_key):
		self.send_blob(blob_key)