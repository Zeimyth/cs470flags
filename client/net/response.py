import abc

class SingleLineResponse(object):
	__metaclass__ = abc.ABCMeta

	""" Messages passed into as the messageArray are expected to come from a server response;
	    that is, they should be in the form "ok <optionalMessage>". If optionalMessage is empty,
	    messageArray should be an empty array. Otherwise, messageArray should be an array
	    containing the message.
	"""
	def __init__(self, messageArray):
		if len(messageArray) == 1:
			self._message = messageArray[0]
			self._hasMessage = True
		else:
			self._hasMessage = False


	def hasMessage(self):
		return self._hasMessage


	def getMessage(self):
		return self._message


	@abc.abstractmethod
	def isOk(self):
		return


	def __str__(self):
		header = None
		content = None

		if self.isOk():
			header = 'Ok'
		else:
			header = 'Fail'

		if self.hasMessage():
			content = self._message
		else:
			content = '<no message>'

		return '({0}) {1}'.format(header, content)



class OkResponse(SingleLineResponse):
	def __init__(self, messageArray):
		SingleLineResponse.__init__(self, messageArray)


	def isOk(self):
		return True



class FailResponse(SingleLineResponse):
	def __init__(self, messageArray):
		SingleLineResponse.__init__(self, messageArray)


	def isOk(self):
		return False



class ListResponse(object):
	def __init__(self, messageArray):
		self._messageList = messageArray


	def getList(self):
		return self._messageList


	def __str__(self):
		return '{0}'.format(self._messageList)
