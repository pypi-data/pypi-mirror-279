import math

"""
Predefined methods
"""

"""
Delay methods
"""


def delay_sin(obj, step):
    return math.sin(math.radians(1.8*step)) * obj.delay


def delay_cos(obj, step):
    return abs(math.cos(math.radians(1.8*step))) * obj.delay


def delay_constant(obj, step):
    return obj.delay


"""
Values methods
"""


def value_on(obj, step):
    """
    Always on at "max" brightness
    """

    return obj.max


def value_off(obj, step):
    """
    Always off
    """

    return 0


def value_linear(obj, step):
    """
    Saw patterned value, 0-1-0
    """

    delta = obj.max - obj.min
    if step < 50:
        return delta*step/50 + obj.min
    else:
        return delta * (100-step)/50 + obj.min


def value_vshape(obj, step):
    """
    V-shape value, 1-0-1
    """

    delta = obj.max - obj.min
    if step < 50:
        return delta * (100-step)/50 + obj.min
    else:
        return delta*step/50 + obj.min


def value_sin(obj, step):
    """
    Sinusoidal values, 0-1-0
    """

    delta = obj.max - obj.min
    radians = math.radians(1.8 * step)
    return delta * math.sin(radians) + obj.min


def value_cos(obj, step):
    """
    Absolute Cosinusoidal values, 1-0-1
    """

    delta = obj.max - obj.min
    radians = math.radians(1.8 * step)
    return delta * abs(math.cos(radians)) + obj.min
