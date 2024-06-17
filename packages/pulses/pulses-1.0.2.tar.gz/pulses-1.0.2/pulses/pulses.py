import logging
import sys
import time
import threading

from queue import Queue
from typing import Callable
from .methods import *  # NOQA


class ledPulse(threading.Thread):

    delayMethods: list = ['constant', 'sin', 'cos']
    valueMethods: list = ['on', 'off', 'linear', 'vshape', 'sin', 'cos']
    methods: dict = {'delay': {}, 'value': {}}

    defaultSet: dict = {
        'min': 2,
        'max': 50,
        'delay': 0.01,
        'delayMethod': 'constant',
        'initialMethod': None,
        'loopMethod': 'linear',
        'finalMethod': None
    }
    initialMethod: str
    loopMethod: str
    finalMethod: str
    delayMethod: str
    min: int
    max: int
    delay: float

    def __init__(self, gpio: int, name: str = "led0") -> None:

        super().__init__(name=name,
                         daemon=True)

        self.log = logging.getLogger(self.__class__.__name__)
        self.gpio = gpio

        self.pwm_setup()

        self.log.info(f"platform '{self.model}' " +
                      f"support: {self.supported}")

        for dm in self.delayMethods:
            self.register_delay_method(dm, eval(f"delay_{dm}"))

        for vm in self.valueMethods:
            self.register_value_method(vm, eval(f"value_{vm}"))

        self.stop_event = threading.Event()

        # Method to stop thread
        # Like
        # def stop():
        #    self.stop_event.set()
        # But shorter ;)
        self.stop = self.stop_event.set

        self.queue = Queue()

        # Set default values
        for key, value in self.defaultSet.items():
            setattr(self, key, value)

    def pwm_setup(self):
        """
        We check if we are running on RPi.
        If yes we set supported to True and set setValue method
        to changeDutyCycle, else
        we set supported to False and create a dummy setValue method
        """

        self.supported = False
        self.model = sys.platform
        try:
            with open('/sys/firmware/devicetree/base/model', 'r') as m:
                model = m.read()[:-1]
                if model.lower().startswith('raspberry pi'):
                    self.supported = True
                    self.model = model
        except Exception:
            pass

        if self.supported:
            import RPi.GPIO as GPIO  # type: ignore
            GPIO.setwarnings(False)          # disable warnings
            GPIO.setmode(GPIO.BCM)           # set pin numbering system
            GPIO.setup(self.gpio, GPIO.OUT)  # set GPIO for output

            # create PWM instance with 120Hz frequency
            self.pwm = GPIO.PWM(self.gpio, 120)
            self.pwm.start(0)  # start pwm with value 0, off
            # setValue function
            self.setValue = self.pwm.ChangeDutyCycle
        else:
            # Platform not supported, set
            # a dummy setValue function
            if self.log.root.level == logging.DEBUG:
                self.setValue = print
            else:
                self.setValue = lambda x: x

        return (self.supported, sys.platform)

    def set(self, **kwargs: dict):

        for key, value in kwargs.items():
            if key in self.defaultSet.keys():
                setattr(self, key, value)
            else:
                self.log.warning(f"set: unknown parameter '{key}'")

        self.log.debug("calculating values: "
                       f"initialMethod:{self.initialMethod}, "
                       f"loopMethod:{self.loopMethod}, "
                       f"finalMethod:{self.finalMethod}, "
                       f"delayMethod:{self.delayMethod}, min:{self.min}, "
                       f"max:{self.max}, delay:{self.delay}")

        delayValues = []
        for step in range(0, 100):
            try:
                delay = self.methods['delay'][self.delayMethod](self, step)
            except NameError:
                self.log.error(f"delay method '{self.delayMethod}' not found")
                return
            delayValues.append(delay)

        initialValues = []
        if self.initialMethod:
            for step in range(0, 50):
                try:
                    value = self.methods['value'][self.initialMethod](self,
                                                                      step)
                except KeyError:
                    self.log.error(f"value method '{self.initialMethod}' "
                                   "not found")
                    return
                initialValues.append((value, delayValues[step]))

        loopValues = []
        for step in range(0, 100):
            try:
                value = self.methods['value'][self.loopMethod](self, step)
            except KeyError:
                self.log.error(f"value method '{self.loopMethod}' not found")
                return
            loopValues.append((value, delayValues[step]))

        finalValues = []
        if self.finalMethod:
            for step in range(50, 100):
                try:
                    value = self.methods['value'][self.finalMethod](self, step)
                except KeyError:
                    self.log.error(f"value method '{self.finalMethod}' "
                                   "not found")
                    return
                finalValues.append((value, delayValues[step]))

        self.queue.put((initialValues, loopValues, finalValues))

    def run(self):

        while True:
            if self.stop_event.is_set():
                self.log.debug("break from main loop, bye")
                if self.supported:
                    self.pwm.stop()
                break

            # Get an item from the queue,
            # if queue is empty, wait for a new item
            # item is a tuple with (initialValues, loopValues, finalValues)
            (initialValues, loopValues, finalValues) = self.queue.get()

            # Initial loop
            self.log.debug('running initial steps')
            for value, delay in initialValues:
                self.setValue(value)
                time.sleep(delay)

            self.log.debug('running main loop')
            while True:
                for value, delay in loopValues:
                    self.setValue(value)
                    time.sleep(delay)

                # After each loop we check if there is something waiting in
                # queue or if stop has been raised
                if not self.queue.empty() or self.stop_event.is_set():
                    break

            self.log.debug('running final steps')
            for value, delay in finalValues:
                self.setValue(value)
                time.sleep(delay)

    ###
    # PLUGINS METHODS
    # We register new functions for delay or value
    # Function must get `step` variable, specifing at which step
    # in the loop we are and is added as a method to self, so
    # it has access to all the properties of self: max, min, delay
    ###
    def register_value_method(self, name: str, fn: Callable):
        self.register_method('value', name, fn)

    def register_delay_method(self, name: str, fn: Callable):
        self.register_method('delay', name, fn)

    def register_method(self, kind: str, name: str, fn: Callable):
        if kind not in ['delay', 'value']:
            self.log.warning(f"unknown kind {kind}")
            return

        if name not in self.methods[kind]:
            self.methods[kind][name] = fn
            self.log.info(f"registered {kind} method '{name}'")
        else:
            self.log.warning(f"{kind} method '{name}' already defined")
