ERROR = 100
WARN = 70
INFO = 50
DEBUG = 30
TRACE = 10

_debugLevel = ERROR

def setDebugLevel(level):
	_debugLevel = level


def setDebugLevelFromString(levelString):
	lowerString = levelString.lower()

	if lowerString == "error":
		setDebugLevel(ERROR)
	elif lowerString == "warn":
		setDebugLevel(WARN)
	elif lowerString == "info":
		setDebugLevel(INFO)
	elif lowerString == "debug":
		setDebugLevel(DEBUG)
	elif lowerString == "trace":
		setDebugLevel(TRACE)


def debugLevelEnabled(level):
	return level >= _debugLevel
