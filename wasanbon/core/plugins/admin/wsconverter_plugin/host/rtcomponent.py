#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- Python -*-

"""
 @file rtcomponent.py
 @brief RT Component
 @date $Date$


"""
import sys, traceback, os
import time
import yaml
sys.path.append(".")

# Import RTM module
import RTC
import OpenRTM_aist

# Import Service implementation class
# <rtc-template block="service_impl">

# import Image

# </rtc-template>

# Import Service stub modules
# <rtc-template block="consumer_import">
# </rtc-template>


# This module's spesification
# <rtc-template block="module_spec">
nao_spec = ["implementation_id", "wsconverter", 
            "type_name",         "wsconverter", 
            "description",       "RT Component", 
            "version",           "1.0.0", 
            "vendor",            "Sugar Sweet Robotics", 
            "category",          "Robot", 
            "activity_type",     "STATIC", 
            "max_instance",      "1", 
            "language",          "Python", 
            "lang_type",         "SCRIPT",
            "conf.default.debug", "0",
            "conf.__widget__.debug", "text",
            ""]
# </rtc-template>

##
# @class 
# @brief RT Component
# 
# 
class wsconverter(OpenRTM_aist.DataFlowComponentBase):
	
	##
	# @brief constructor
	# @param manager Maneger Object
	# 
	def __init__(self, manager):
		OpenRTM_aist.DataFlowComponentBase.__init__(self, manager)
                """
		self._d_velocity = RTC.TimedVelocity2D(RTC.Time(0,0), RTC.Velocity2D(0,0,0))
		self._velocityIn = OpenRTM_aist.InPort("velocity", self._d_velocity)
                """
		# initialize of configuration-data.
		# <rtc-template block="init_conf_param">
		"""
		"""
		self._debgu = ['0']

		self.loaded_modules = {}

		# </rtc-template>
	##
	#
	# The initialize action (on CREATED->ALIVE transition)
	# formaer rtc_init_entry() 
	# 
	# @return RTC::ReturnCode_t
	# 
	#
	def onInitialize(self):

		# Bind variables and configuration variable
                # self.bindParameter("ipaddress", self._ipaddress, "nao.local")

		# Set InPort buffers
                # self.addInPort("velocity", self._velocityIn)

		# Set OutPort buffers
		
		# Set service provider to Ports

		# Set service consumers to Ports
		
		# Set CORBA Service Ports

		return RTC.RTC_OK
	
	#	##
	#	# 
	#	# The finalize action (on ALIVE->END transition)
	#	# formaer rtc_exiting_entry()
	#	# 
	#	# @return RTC::ReturnCode_t
	#
	#	# 
	#def onFinalize(self, ec_id):
	#
	#	return RTC.RTC_OK
	
	#	##
	#	#
	#	# The startup action when ExecutionContext startup
	#	# former rtc_starting_entry()
	#	# 
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#
	#	#
	#def onStartup(self, ec_id):
	#
	#	return RTC.RTC_OK
	
	#	##
	#	#
	#	# The shutdown action when ExecutionContext stop
	#	# former rtc_stopping_entry()
	#	#
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#
	#	#
	#def onShutdown(self, ec_id):
	#
	#	return RTC.RTC_OK
	
		##
		#
		# The activated action (Active state entry action)
		# former rtc_active_entry()
		#
		# @param ec_id target ExecutionContext Id
		# 
		# @return RTC::ReturnCode_t
		#
		#
	def onActivated(self, ec_id):

		return RTC.RTC_OK
	
		##
		#
		# The deactivated action (Active state exit action)
		# former rtc_active_exit()
		#
		# @param ec_id target ExecutionContext Id
		#
		# @return RTC::ReturnCode_t
		#
		#
	def onDeactivated(self, ec_id):

		return RTC.RTC_OK
	
		##
		#
		# The execution action that is invoked periodically
		# former rtc_active_do()
		#
		# @param ec_id target ExecutionContext Id
		#
		# @return RTC::ReturnCode_t
		#
		#
	def onExecute(self, ec_id):

		return RTC.RTC_OK
	
	#	##
	#	#
	#	# The aborting action when main logic error occurred.
	#	# former rtc_aborting_entry()
	#	#
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#
	#	#
	#def onAborting(self, ec_id):
	#
	#	return RTC.RTC_OK
	
	#	##
	#	#
	#	# The error action in ERROR state
	#	# former rtc_error_do()
	#	#
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#
	#	#
	#def onError(self, ec_id):
	#
	#	return RTC.RTC_OK
	
	#	##
	#	#
	#	# The reset action that is invoked resetting
	#	# This is same but different the former rtc_init_entry()
	#	#
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#
	#	#
	#def onReset(self, ec_id):
	#
	#	return RTC.RTC_OK
	
	#	##
	#	#
	#	# The state update action that is invoked after onExecute() action
	#	# no corresponding operation exists in OpenRTm-aist-0.2.0
	#	#
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#

	#	#
	#def onStateUpdate(self, ec_id):
	#
	#	return RTC.RTC_OK
	
	#	##
	#	#
	#	# The action that is invoked when execution context's rate is changed
	#	# no corresponding operation exists in OpenRTm-aist-0.2.0
	#	#
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#
	#	#
	#def onRateChanged(self, ec_id):
	#
	#	return RTC.RTC_OK
	
	def load(self, modulename):
		module_dir = 'modules'
		print 'Loading -', modulename
		import handler
		self._ws = handler.ws
		import imp
		try:
			sys.path.insert(0, os.path.join(os.getcwd(), module_dir))
			file, pathname, description = imp.find_module(modulename)
			m = imp.load_module(modulename, file, pathname, description)
			m.execute(self, self._ws)
			self.loaded_modules[modulename] = m
		except:
			sys.stdout.write('# Loading Plugin (%s) Failed.\n' % modulename)
			traceback.print_exc()
		return None

	def removeAllPort(self):
		for inport in self._inports:
			print 'removing ', inport
			print self.removePort(inport)

		for outport in self._outports:
			print 'removing ', outport
			print self.removePort(outport)

component = None

def wsconverterInit(manager):
    profile = OpenRTM_aist.Properties(defaults_str=nao_spec)
    manager.registerFactory(profile,
                            wsconverter,
                            OpenRTM_aist.Delete)

def MyModuleInit(manager):
    wsconverterInit(manager)

    # Create a component
    global component
    component = manager.createComponent("wsconverter?naming.formats=%n.rtc&logger.enable=NO")


def main(argv=[]):
	mgr = OpenRTM_aist.Manager.init(argv)
	mgr.setModuleInitProc(MyModuleInit)
	mgr.activateManager()
	mgr.runManager(True)

if __name__ == "__main__":
	main()

