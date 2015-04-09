# -*- coding: utf-8 -*-
# Base class for all loadable modules

#* do not die during module loading in any case, and therefore do nothing!!!
#* initialise module
#* identify yourself
#* output redirection (instead of print)
#* de-initialise yourself
#* reload the module with code changes
#* get your own configuration (for save)
#* get name of status variables
#* get status variables
#* reload module data (from saved variables)
#* Pyro interconnection


from pyqtgraph.Qt import QtCore
from fysom import Fysom

class Base(QtCore.QObject, Fysom):
    _modclass = 'base'
    _modtype = 'base'

    def __init__(self, manager, name, configuration = {}, callback_dict = {}, **kwargs):

        # Qt signal/slot capabilities
        QtCore.QObject.__init__(self)
        
        # State machine definition
        __baseStateList = {
            'initial': 'deactivated',
            'events': [
                {'name': 'activate', 'src': 'deactivated', 'dst': 'idle' },
                {'name': 'deactivate', 'src': 'idle', 'dst': 'deactivated' },
                {'name': 'deactivate', 'src': 'running', 'dst': 'deactivated' },
                {'name': 'run', 'src': 'idle', 'dst': 'running' },
                {'name': 'stop', 'src': 'running', 'dst': 'idle' },
                {'name': 'lock', 'src': 'idle', 'dst': 'locked' },
                {'name': 'lock', 'src': 'running', 'dst': 'locked' },
                {'name': 'block', 'src': 'idle', 'dst': 'blocked' },
                {'name': 'block', 'src': 'running', 'dst': 'blocked' },
                {'name': 'blocktolock', 'src': 'locked', 'dst': 'blocked' },
                {'name': 'unlock', 'src': 'locked', 'dst': 'idle' },
                {'name': 'unblock', 'src': 'blocked', 'dst': 'idle' },
                {'name': 'runlock', 'src': 'locked', 'dst': 'running' },
                {'name': 'runblock', 'src': 'blocked', 'dst': 'running' }
            ],
            'callbacks': callback_dict
        }

        Fysom.__init__(self, __baseStateList)

        self._manager = manager
        self._name = name
        self._configuration = configuration

    def activate(self):
        self.logMsg("Please implement this function.", messageType='status')

    def deactivate(self):
        self.logMsg("Please implement this function.", messageType='status')

    def getStatusVariableList(self):
        self.logMsg("Please implement this function.", messageType='status')
        return list()

    def getStatusVariables(self):
        self.logMsg("Please implement this function.", messageType='status')
        return dict()

    # Do not replace these in subclasses

    def getState(self):
        return self._state.current

    def getConfguration(self):
        return _configuration

    def logMsg(self, message, messageType='status'):
        self._manager.logger.logMsg('%s.%s: %s' % (_modclass, _modtype, message), msgType=messageType)

    @staticmethod
    def identify():
        return {moduleclass: _class, moduletype: _modtype}
