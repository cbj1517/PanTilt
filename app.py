import os

import cherrypy
from cherrypy.lib.static import serve_file

import Adafruit_BBIO.PWM as PWM

pan_pin = "P8_13"
tilt_pin = "P8_19"
duty_min = 3
duty_max = 14.5
duty_span = duty_max-duty_min
pAngle = 90.0
tAngle = 90.0
 
path   = os.path.abspath(os.path.dirname(__file__))
config = {
  'global' : {
    'server.socket_host' : '0.0.0.0',
    'server.socket_port' : 8000,
    'server.thread_pool' : 8
  }
}

class App:

  @cherrypy.expose
  def index(self):
    return serve_file(os.path.join(path, 'index.html')) 

  @cherrypy.expose
  @cherrypy.tools.json_out()
  def mvUP(self):
    print "up"

    global tAngle
    tAngle = tAngle - 5
    tDuty = 100-((tAngle/180)*duty_span + duty_min)	
    PWM.set_duty_cycle(tilt_pin, tDuty)
	
  @cherrypy.expose
  @cherrypy.tools.json_out()
  def mvDN(self):
    print "down"

    global tAngle
    tAngle = tAngle + 5
    tDuty = 100-((tAngle/180)*duty_span + duty_min)	
    PWM.set_duty_cycle(tilt_pin, tDuty)
	
  @cherrypy.expose
  @cherrypy.tools.json_out()
  def mvLF(self):
    print "left"

    global pAngle
    pAngle = pAngle + 5
    pDuty = 100-((pAngle/180)*duty_span + duty_min)
    PWM.set_duty_cycle(pan_pin, pDuty)	
	
  @cherrypy.expose
  @cherrypy.tools.json_out()
  def mvRT(self):
    print "right"

    global pAngle
    pAngle = pAngle - 5
    pDuty = 100-((pAngle/180)*duty_span + duty_min)
    PWM.set_duty_cycle(pan_pin, pDuty)	
	
  @cherrypy.expose
  @cherrypy.tools.json_out()
  def mvHM(self):
    print "home"

    global pAngle
    global tAngle
    #move servos to home positions
    pAngle = 80.0
    tAngle = 70.0
    pDuty = 100-((pAngle/180)*duty_span + duty_min)
    tDuty = 100-((tAngle/180)*duty_span + duty_min)

    PWM.set_duty_cycle(pan_pin, pDuty)
    PWM.set_duty_cycle(tilt_pin, tDuty)	

  @cherrypy.expose
  @cherrypy.tools.json_out()
  def shutDown(self):
    #shutdown PWM cleanly
    PWM.stop(pan_pin)
    PWM.stop(tilt_pin)
    PWM.cleanup()
    #shutdown cherrypy cleanly
    cherrypy.engine.exit()

  @cherrypy.expose
  @cherrypy.tools.json_out()
  def startPWM(self):
    PWM.start(pan_pin,(100-duty_min), 60.0, 1)
    PWM.start(tilt_pin, (100-duty_min), 60.0, 1)
	
move = App()
move.startPWM()
#move.mvHM()

if __name__ == '__main__':
  cherrypy.quickstart(App(), '/', config)
