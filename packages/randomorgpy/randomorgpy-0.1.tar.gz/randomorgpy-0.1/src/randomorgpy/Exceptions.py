## @package randomorgpy

## @brief Exception class for invalid values
# @details Exception used if a value has to be one of a specific list.
# @author Felix Hune
# @version 0.1
# @date 2024-06-14
class WrongValueException(Exception):
    def __init__(self, base, rang):
        self.base = base
        self.message = "Value should be one of " + str(rang) + ". You entered: " + str(base)
        super().__init__(self.message)

## @brief Exception class for values exceeding length
# @details Exception used if a values length exceeds limits
# @author Felix Hune
# @version 0.1
# @date 2024-06-14
class WrongLengthException(Exception):
    def __init__(self, length, minimum, maximum):
        self.length = length
        self.message = ("Length should be between " + str(minimum) + " and " + str(maximum) +
                        ". You entered: " + str(length))
        super().__init__(self.message)

## @brief Exception class for values exceeding range
# @details Exception used if a value exceeds a range
# @author Felix Hune
# @version 0.1
# @date 2024-06-14
class WrongRangeException(Exception):
    def __init__(self, value, minimum, maximum):
        self.value = value
        self.message = ("Value should be between " + str(minimum) + " and " + str(maximum) +
                        ". You entered: " + str(value))
        super().__init__(self.message)
