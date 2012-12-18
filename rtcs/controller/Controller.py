#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- Python -*-

"""
 \file Controller.py
 \brief OpenTPR Controller RTC
 \date $Date$


"""
import sys
import time
from xml.dom import minidom, Node
sys.path.append(".")

# Import RTM module
import RTC
import OpenRTM_aist
#from xml2dict import  *

# Import Service implementation class
# <rtc-template block="service_impl">

# </rtc-template>

# Import Service stub modules
# <rtc-template block="consumer_import">
# </rtc-template>


# This module's spesification
# <rtc-template block="module_spec">
controller_spec = ["implementation_id", "Controller", 
		 "type_name",         "Controller", 
		 "description",       "OpenTPR Controller RTC", 
		 "version",           "1.0.0", 
		 "vendor",            "SugarSweetRobotics", 
		 "category",          "Experimenta", 
		 "activity_type",     "STATIC", 
		 "max_instance",      "1", 
		 "language",          "Python", 
		 "lang_type",         "SCRIPT",
		 ""]
# </rtc-template>

class Controller(OpenRTM_aist.DataFlowComponentBase):
	
	"""
	\class Controller
	\brief OpenTPR Controller RTC
	
	"""
	def __init__(self, manager):
		"""
		\brief constructor
		\param manager Maneger Object
		"""
		OpenRTM_aist.DataFlowComponentBase.__init__(self, manager)

		self._d_velIn = RTC.TimedVelocity2D(RTC.Time(0,0),RTC.Velocity2D(0, 0, 0))
		"""
		"""
		self._velInIn = OpenRTM_aist.InPort("velIn", self._d_velIn)
		self._d_octetIn = RTC.TimedOctetSeq(RTC.Time(0,0),"")
		"""
		"""
		self._octetInIn = OpenRTM_aist.InPort("octetIn", self._d_octetIn)
		self._d_velOut = RTC.TimedVelocity2D(RTC.Time(0,0), [])
		"""
		"""
		self._velOutOut = OpenRTM_aist.OutPort("velOut", self._d_velOut)
		self._d_octetOut = RTC.TimedOctetSeq(RTC.Time(0,0), "")
		"""
		"""
		self._octetOutOut = OpenRTM_aist.OutPort("octetOut", self._d_octetOut)


		


		# initialize of configuration-data.
		# <rtc-template block="init_conf_param">
		
		# </rtc-template>


		 
	def onInitialize(self):
		"""
		
		The initialize action (on CREATED->ALIVE transition)
		formaer rtc_init_entry() 
		
		\return RTC::ReturnCode_t
		
		"""
		# Bind variables and configuration variable
		
		# Set InPort buffers
		self.addInPort("velIn",self._velInIn)
		self.addInPort("octetIn",self._octetInIn)
		
		# Set OutPort buffers
		self.addOutPort("velOut",self._velOutOut)
		self.addOutPort("octetOut",self._octetOutOut)
		
		# Set service provider to Ports
		
		# Set service consumers to Ports
		
		# Set CORBA Service Ports
		
		return RTC.RTC_OK
	
	#def onFinalize(self, ec_id):
	#	"""
	#
	#	The finalize action (on ALIVE->END transition)
	#	formaer rtc_exiting_entry()
	#
	#	\return RTC::ReturnCode_t
	#
	#	"""
	#
	#	return RTC.RTC_OK
	
	#def onStartup(self, ec_id):
	#	"""
	#
	#	The startup action when ExecutionContext startup
	#	former rtc_starting_entry()
	#
	#	\param ec_id target ExecutionContext Id
	#
	#	\return RTC::ReturnCode_t
	#
	#	"""
	#
	#	return RTC.RTC_OK
	
	#def onShutdown(self, ec_id):
	#	"""
	#
	#	The shutdown action when ExecutionContext stop
	#	former rtc_stopping_entry()
	#
	#	\param ec_id target ExecutionContext Id
	#
	#	\return RTC::ReturnCode_t
	#
	#	"""
	#
	#	return RTC.RTC_OK
	
	def onActivated(self, ec_id):
		"""
	
		The activated action (Active state entry action)
		former rtc_active_entry()
	
		\param ec_id target ExecutionContext Id
	
		\return RTC::ReturnCode_t
	
		"""
	
		return RTC.RTC_OK
	
	def onDeactivated(self, ec_id):
		"""
	
		The deactivated action (Active state exit action)
		former rtc_active_exit()
	
		\param ec_id target ExecutionContext Id
	
		\return RTC::ReturnCode_t
	
		"""
	
		return RTC.RTC_OK
	
	def onExecute(self, ec_id):
		"""
	
		The execution action that is invoked periodically
		former rtc_active_do()
	
		\param ec_id target ExecutionContext Id
	
		\return RTC::ReturnCode_t
	
		"""

		if self._velInIn.isNew():
			v = self._velInIn.read()
			print "Vel %f %f %f" % (v.data.vx, v.data.vy, v.data.va)
			
			#vstr = """<DataPortPacket name="velOut"><Member name="data"><Member name="vx">%f</Member><Member name="vy">%f</Member><Member name="va">%f</Member></Member></DataPortPacket>""" % (v.data.vx, v.data.vy, v.data.va)
			vstr = "<data><vx>%f</vx><vy>%f</vy><va>%f</va></data>" % (v.data.vx, v.data.vy, v.data.va)
			print vstr
			self._d_octetOut.data = vstr
			self._octetOutOut.write()
		
		
		if self._octetInIn.isNew():
			d = self._octetInIn.read()
			vx = doc.childNodes[0].childNodes[0].childNodes[0].wholeText
			vy = doc.childNodes[0].childNodes[1].childNodes[0].wholeText
			va = doc.childNodes[0].childNodes[2].childNodes[0].wholeText

			self._d_velOut.data = RTC.Velocity2D(float(vx), float(vy), float(va))
			self._velOutOut.write()
			
	
		return RTC.RTC_OK
	
	#def onAborting(self, ec_id):
	#	"""
	#
	#	The aborting action when main logic error occurred.
	#	former rtc_aborting_entry()
	#
	#	\param ec_id target ExecutionContext Id
	#
	#	\return RTC::ReturnCode_t
	#
	#	"""
	#
	#	return RTC.RTC_OK
	
	#def onError(self, ec_id):
	#	"""
	#
	#	The error action in ERROR state
	#	former rtc_error_do()
	#
	#	\param ec_id target ExecutionContext Id
	#
	#	\return RTC::ReturnCode_t
	#
	#	"""
	#
	#	return RTC.RTC_OK
	
	def onReset(self, ec_id):
		"""
	
		The reset action that is invoked resetting
		This is same but different the former rtc_init_entry()
	
		\param ec_id target ExecutionContext Id
	
		\return RTC::ReturnCode_t
	
		"""
	
		return RTC.RTC_OK
	
	#def onStateUpdate(self, ec_id):
	#	"""
	#
	#	The state update action that is invoked after onExecute() action
	#	no corresponding operation exists in OpenRTm-aist-0.2.0
	#
	#	\param ec_id target ExecutionContext Id
	#
	#	\return RTC::ReturnCode_t
	#
	#	"""
	#
	#	return RTC.RTC_OK
	
	#def onRateChanged(self, ec_id):
	#	"""
	#
	#	The action that is invoked when execution context's rate is changed
	#	no corresponding operation exists in OpenRTm-aist-0.2.0
	#
	#	\param ec_id target ExecutionContext Id
	#
	#	\return RTC::ReturnCode_t
	#
	#	"""
	#
	#	return RTC.RTC_OK
	



def ControllerInit(manager):
    profile = OpenRTM_aist.Properties(defaults_str=controller_spec)
    manager.registerFactory(profile,
                            Controller,
                            OpenRTM_aist.Delete)

def MyModuleInit(manager):
    ControllerInit(manager)

    # Create a component
    comp = manager.createComponent("Controller")

def main():
	mgr = OpenRTM_aist.Manager.init(sys.argv)
	mgr.setModuleInitProc(MyModuleInit)
	mgr.activateManager()
	mgr.runManager()

if __name__ == "__main__":
	main()

