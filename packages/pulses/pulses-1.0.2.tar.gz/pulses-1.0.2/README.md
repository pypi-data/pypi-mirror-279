# Pulses

Pulses is a python module to drive LEDs on RPi using PWM (Pulse Width Modulation)

### BUILD

1. Clone the repo

   `https://gitea.mistrali.pw/musicalbox/pulses.git`

3. `pip install requirements-dev.txt`
4. `poetry build`
5. `pip install dist/pulses-<version>-py3-none-any.whl`


### GPIO and PWM
For more info on PWM refer to [PWM](https://en.wikipedia.org/wiki/Pulse-width_modulation) and for information on the different GPIO pin you can read [this](https://projects.raspberrypi.org/en/projects/physical-computing/1).


### CLI tool

There is a CLI tool, called `pulses` that you can use to test loops and pulses.
Run `pulses -h` to read the usage instructions.

### Work model

Each `ledPulse` object has some attributes that define the **pulse**, i.e. the light pattern of the managed LED.

The state of the LED is controlled by the following parameters:
- **min**: minimum brightness value, I suggest to avoid using `0`, start from `2`;
- **max**: maximum brightness;
- **delay**: the base delay between each step of the pattern;
- **initialMethod**: the method used to calculate the initial steps of the pattern;
- **loopMethod**: the method used to calculate the steps of the main loop;
- **finalMethod**: the method used to calculate the final steps of the loop;
- **delayMethod**: the method used to calculate the delay between each step;

Each pattern starts running 50 steps of initial values, then goes into a repeteated loop, on exit it runs other 50 steps of final values.

To change the above parameters we use a FIFO queue, each time we `set` a new value of one of the above attributes, `ledPulse` will calculate a `tuple` of 3 values, each element of the tuple is in turn an array of 2-ples, each of these 2-ples has the first element as the `value` at a specific step, the second element is the `delay` at a specific step.

- `initialValues`: 50 elements, if an initialMethod is defined, empy otherwise. These are the values that define the pattern of the LED at the start of the new loop;
- `loopValues`: 100 elements, never empy. These are the values that define the pattern of the LED at the core infinite loop;
- `finalValues`: 50 elements, if a finalMethod is defined, empy otherwise. These are the values that define the pattern of the LED at the end of a terminating loop;

#### An example

Let's say we define a new pattern that has:
- `initialMethod = linear`;
- `loopMethod = cos`;
- `finalMethod = linear`;
- `delayMethod = constant`;
- `delay = 0.01`;
- `min = 2`;
- `max = 50`;

The LED starts from brightness `0`, in 50 steps goes linearly to brightness `50`, i.e. the brightness will increate of 1 at each step, there is a delay of `0.01` seconds between each step.
After these first 50 steps, there will be a repeating loop, looping on `cosine` values, so going from brightness 50 (value of max), down to brightness 2 (value of min), the up again to brightness 50, still with a constant delay of 0.01 between each step.
The moment we will add a new tuple of values to the queue, using the `set()` method, the worker will exit from the repeating loop, run on 50 steps of the final values and then start with a new similar loop with the new values.

### Class

The only class defined is called `ledPulse`, it is derived from `threading.Thread`
and takes care of managing the led connected to a PWM GPIO.

#### Methods
`__init__`: quite simple, the only parameter is the GPIO pin we want to use. This method takes care of:
- setting up logging;
- setting up PWM;
- installing the default methods for loops and delays;
- set up the queue that we will use later on;

`set()`: change one or more parameter of the state. Bear in mind that each parameter is standalone, so if `min` is set to `2` and `max` is set to `20`, calling `led.set(max=40)` will only change the value of `max` parameter, leaving all the others at the previous value. After successfully setting a parameter, the values for `initial`, `loop`, `final` and `delay` are recalculated and a new tuple is added to the queue;

`run`: this method runs the main loop, that executes first a loop of 50 steps with `initialValues` if this is not empty, then loops on `loopValues` until there is a new tuple in the queue OR the `stop_event` event is set. If there is a new tuple in the queue, the infinite loop on `loopValues` is interrupted, another loop of 50 steps runs through `finalValues` (if not empty) and then we go to the main loop, pull the tuple from the queue and start all over, unless `stop_event` is set; if that's the case we bail out of the external loop and the thread is going to stop;

#### Plugins
Pulses uses `plugin methods` to calculate the values and delays for each loop.
These plugin methods are nothing more than python functions, following this prototypes:

- for value plugins:
```python
def value_methodname(obj, step):
    return <value for step>
```

- for delay plugins:
```python
def delay_methodname(obj, step):
    return <delay value for step>
```

`obj` is the LED object that uses the method, so you can refer to the attributes of if, like `obj.max` or `obj.min`.

Some examples, that are predefined in Pulses:

```python
def delay_constant(obj, step):
    # Delay method: constant
    return obj.delay

def value_sin(obj, step):
    """
    Value method: sin
    Sinusoidal values, 0-1-0 /\
    """

    delta = obj.max - obj.min
    radians = math.radians(1.8 * step)
    return delta * math.sin(radians) + obj.min

def value_on(obj, step):
    """
    Value method: on
    Always on at "max" brightness
    """

    return obj.max
```

You can write your own method plugins, trying to keep them quite simple possibly, then you have to register them before being able to use them.
You can use two specific methods to register plugins based on their kind:

- `register_delay_method(methodName, function)`;
- `register_value_method(methodName, function)`;

For example, we can write a function that returns a random value between `min` and `max`:

in `mymodule.py`:
```python
def value_random(obj, step):
    return random.randint(obj.min, obj.max)
```

then we can register it

```python
from pulses import ledPulse
from mymodule import value_random

led = ledPulse(12)
led.register_value_method('random', value_random)
led.set(loopMethod='random')
```

from now on we can call `led.set(loopValue='random')` and our LED will blink with a random value at each step.
