## @package randomorgpy
import json
import requests
import random
from .Exceptions import *

## @brief Client object holding all methods for the api
# @details This class is the Client object, which contains all methods that are used for the api. It also stores the api key (token) and an id (id)
# @author Felix Hune
# @version 0.1
# @date 2024-06-14
class Client:
    
    url = "https://api.random.org/json-rpc/4/invoke"
    
    ## @param   token   The api key / token for the random.org api
    # @author Felix Hune
    # @date 2024-06-14
    def __init__(self, token: str):
        self.token = token
        self.id = random.randint(0, 1000)
    
    ## @brief Get the stored api token
    # @return @p str
    def getToken(self):
        return self.token
    
    ## @brief Set the stored api token
    # @param    token   A new api key / token for the api
    def setToken(self, token: str):
        self.token = token
    
    ## @brief Get the stored id
    # @return @p int
    def getId(self):
        return self.id
    
    ## @brief Set a new id
    # @param    id  A new id
    def setId(self, ident: int):
        self.id = ident
    
    ## @brief Does the actual api request
    # @private
    def _req(self, method: str, **params):
        raw_data = {"method": method, "jsonrpc": "2.0",
                    "id": self.id, "params": {"apiKey": self.token}}
        for key in params:
            raw_data["params"][key] = params[key]
        data = json.dumps(raw_data)
        headers = {"Content-Type": "application/json"}
        r = requests.post(self.url, data=data, headers=headers)
        return r.json()

    @staticmethod
    ## @brief checks if kwarg exists and returns it, else returns default value
    # @private
    def _dekwarg(kwargs, key, default):
        if key in kwargs:
            return kwargs[key]
        return default

    ## @brief Generate Integers
    # @details Generate a given number of integers within given borders
    # @param    n           Count of numbers to generate (1 to 10000)
    # @param    minimum     The minimum for each number (-1E9 to 1E9)
    # @param    maximum     The maximum for each number (-1E9 to 1E9)
    # @param    base        <b>Keyword Argument</b> This defines the base the numbers should be in (one of (2,8,10,16)). Default is @p 10.
    # @param    replacement <b>Keyword Argument</b> This defines wether values are allowed to occure multiple times or not. Defaults to @p True.
    # @param    simple      <b>Keyword Argument</b> This defines wether the response should be simple styled or the full response. Defaults to @p False.
    # @return Either a @p dict in json format or a @p list
    # @author Felix Hune
    # @version 0.1
    # @date 2024-06-14
    def genInt(self, n: int, minimum: int, maximum: int, **kwargs):
        base = self._dekwarg(kwargs, "base", 10)
        replacement = self._dekwarg(kwargs, "replacement", True)
        simple = self._dekwarg(kwargs, "simple", False)
        if base not in [2, 8, 10, 16]:
            raise WrongValueException(base, [2, 8, 10, 16])
        if n < 1 or n > 10000:
            raise WrongRangeException(n, 1, 10000)
        if minimum < -1000000000 or minimum > 1000000000:
            raise WrongRangeException(minimum, -1000000000, 1000000000)
        if maximum < -1000000000 or maximum > 1000000000:
            raise WrongRangeException(maximum, -1000000000, 1000000000)
        res = self._req("generateIntegers", n=n, min=minimum, max=maximum, base=base, replacement=replacement)
        if simple:
            return res["result"]["random"]["data"]
        return res
    
    ## @brief Generate Integer Sequences
    # @details Generate a given number of integer sequences of given length within given borders
    # @param    n           Count of sequences to generate (1 to 1000)
    # @param    length      Count of numbers per sequence (1 to 10000)
    # @param    minimum     The minimum for each number (-1E9 to 1E9)
    # @param    maximum     The maximum for each number (-1E9 to 1E9)
    # @param    base        <b>Keyword Argument</b> This defines the base the numbers should be in (one of (2,8,10,16)). Default is @p 10.
    # @param    replacement <b>Keyword Argument</b> This defines wether values are allowed to occure multiple times or not. Defaults to @p True.
    # @param    simple      <b>Keyword Argument</b> This defines wether the response should be simple styled or the full response. Defaults to @p False.
    # @return Either a @p dict in json format or a @p list of @p lists
    # @author Felix Hune
    # @version 0.1
    # @date 2024-06-14
    def genIntSeq(self, n: int, length: int, minimum: int, maximum: int, **kwargs):
        base = self._dekwarg(kwargs, "base", 10)
        replacement = self._dekwarg(kwargs, "replacement", True)
        simple = self._dekwarg(kwargs, "simple", False)
        if base not in [2, 8, 10, 16]:
            raise WrongValueException(base, [2, 8, 10, 16])
        if n < 1 or n > 1000:
            raise WrongRangeException(n, 1, 1000)
        if length < 1 or length > 10000:
            raise WrongLengthException(length, 1, 10000)
        if minimum < -1000000000 or minimum > 1000000000:
            raise WrongRangeException(minimum, -1000000000, 1000000000)
        if maximum < -1000000000 or maximum > 1000000000:
            raise WrongRangeException(maximum, -1000000000, 1000000000)
        res = self._req("generateIntegerSequences", n=n, length=length, min=minimum, max=maximum, base=base,
                        replacement=replacement)
        if simple:
            return res["result"]["random"]["data"]
        return res
        
    ## @brief Generate Decimal Fractions
    # @details Generate a given number of decimal fractions between 0 and 1 with a given number of decimal places
    # @param    n               Count of numbers to generate (1 to 10000)
    # @param    decimalPlaces   Count of decimal places for each number (1 to 14)
    # @param    replacement     <b>Keyword Argument</b> This defines wether values are allowed to occure multiple times or not. Defaults to @p True.
    # @param    simple          <b>Keyword Argument</b> This defines wether the response should be simple styled or the full response. Defaults to @p False.
    # @return Either a @p dict in json format or a @p list
    # @author Felix Hune
    # @version 0.1
    # @date 2024-06-14
    def genDecFrac(self, n: int, decimalPlaces: int, **kwargs):
        replacement = self._dekwarg(kwargs, "replacement", True)
        simple = self._dekwarg(kwargs, "simple", False)
        if n < 1 or n > 10000:
            raise WrongRangeException(n, 1, 10000)
        if decimalPlaces < 1 or decimalPlaces > 14:
            raise WrongRangeException(decimalPlaces, 1, 14)
        res = self._req("generateDecimalFractions", n=n, decimalPlaces=decimalPlaces, replacement=replacement)
        if simple:
            return res["result"]["random"]["data"]
        return res
    
    ## @brief Generate Gaussian Distribution Numbers
    # @details Generate a given number of random numbers from a Gaussian distribution with given mean and standard deviation values.
    # @param    n                   Count of numbers to generate (1 to 10000)
    # @param    mean                Mean value of the Gaussian distribution (-1E6 to 1E6)
    # @param    standardDeviation   Standard deviation value of the Gaussian distribution (-1E6 to 1E6)
    # @param    significantDigits   Count of significant digits (2 to 14)
    # @param    simple              <b>Keyword Argument</b> This defines wether the response should be simple styled or the full response. Defaults to @p False.
    # @return Either a @p dict in json style or a @p list
    # @author Felix Hune
    # @version 0.1
    # @date 2024-06-14
    def genGauss(self, n: int, mean: int, standardDeviation: int, significantDigits: int, **kwargs):
        simple = self._dekwarg(kwargs, "simple", False)
        if n < 1 or n > 10000:
            raise WrongRangeException(n, 1, 10000)
        if mean < -1000000 or mean > 1000000:
            raise WrongRangeException(mean, -1000000, 1000000)
        if standardDeviation < -1000000 or standardDeviation > 1000000:
            raise WrongRangeException(standardDeviation, -1000000, 1000000)
        if significantDigits < 2 or significantDigits > 14:
            raise WrongRangeException(significantDigits, 2, 14)
        res = self._req("generateGaussians", n=n, mean=mean, standardDeviation=standardDeviation,
                        significantDigits=significantDigits)
        if simple:
            return res["result"]["random"]["data"]
        return res
    
    ## @brief Generate random strings
    # @details Generate a given number of strings with given length consisting of given chars
    # @param    n           Count of strings to generate (1 to 10000)
    # @param    length      The length of the strings (1 to 32)
    # @param    characters  A string containing the characters to include in generation (max 128)
    # @param    replacement <b>Keyword Argument</b> This defines wether values are allowed to occure multiple times or not. Defaults to @p True.
    # @param    simple      <b>Keyword Argument</b> This defines wether the response should be simple styled or the full response. Defaults to @p False.
    # @return Either a @p dict in json style or a @p list
    # @author Felix Hune
    # @version 0.1
    # @date 2024-06-14
    def genStr(self, n: int, length: int, characters: str, **kwargs):
        replacement = self._dekwarg(kwargs, "replacement", True)
        simple = self._dekwarg(kwargs, "simple", False)
        if n < 1 or n > 10000:
            raise WrongRangeException(n, 1, 10000)
        if length < 1 or length > 32:
            raise WrongLengthException(length, 1, 32)
        if len(characters) < 1 or len(characters) > 128:
            raise WrongLengthException(len(characters), 1, 128)
        res = self._req("generateStrings", n=n, length=length, characters=characters, replacement=replacement)
        if simple:
            return res["result"]["random"]["data"]
        return res
        
    ## @brief Generate random UUIDs
    # @details Generate a given number of UUIDs
    # @param    n       Count of UUIDs to generate (1 to 1000)
    # @param    simple  <b>Keyword Argument</b> This defines wether the response should be simple styled or the full response. Defaults to @p False.
    # @return Either a @p dict in json style or a @p list
    # @author Felix Hune
    # @version 0.1
    # @date 2024-06-14
    def genUUID(self, n: int, **kwargs):
        simple = self._dekwarg(kwargs, "simple", False)
        if n < 1 or n > 1000:
            raise WrongRangeException(n, 1, 1000)
        res = self._req("generateUUIDs", n=n)
        if simple:
            return res["result"]["random"]["data"]
        return res

    ## @brief Generate random BLOBs
    # @details Generate a given number of BLOBs of given size in bits
    # @param    n           Count of BLOBs to generate (1 to 100)
    # @param    size        The size of each blob (1 to 1048576 bits, must be divisible by 8). Additionally, the total size must not exceed 1048576 bits.
    # @param    form        <b>Keyword Argument</b> This defines the format of the response. Must be one of (base64, hex). Defaults to @p base64.
    # @param    simple      <b>Keyword Argument</b> This defines wether the response should be simple styled or the full response. Defaults to @p False.
    # @return Either a @p dict in json style or a @p list
    # @author Felix Hune
    # @version 0.1
    # @date 2024-06-14
    def genBlob(self, n: int, size: int, **kwargs):
        form = self._dekwarg(kwargs, "form", "base64")
        simple = self._dekwarg(kwargs, "simple", False)
        if form not in ["base64", "hex"]:
            raise WrongValueException(form, ["base64", "hex"])
        if n < 1 or n > 100:
            raise WrongRangeException(n, 1, 100)
        if size < 1 or size > 1048576:
            raise WrongRangeException(size, 1, 1048576)
        if size % 8 != 0:
            raise ValueError("Size must be a multiple of 8")
        if n * size > 1048576:
            raise ValueError("Total size must be less than 1048576 bits")
        res = self._req("generateBlobs", n=n, size=size, format=form)
        if simple:
            return res["result"]["random"]["data"]
        return res
    
    ## @brief Get usage statistics
    # @details Get the usage statistics for this api key
    # @param    simple  <b>Keyword Argument</b> This defines wether the response should be simple styled or the full response. Defaults to @p False.
    # @return   A @p dict in json style
    # @author Felix Hune
    # @version 0.1
    # @date 2024-06-14
    def getUsage(self, **kwargs):
        simple = self._dekwarg(kwargs, "simple", False)
        res = self._req("getUsage")
        if simple:
            return res["result"]
        return res

    def __str__(self):
        return "Client with token: " + self.token + " and id: " + str(self.id)
