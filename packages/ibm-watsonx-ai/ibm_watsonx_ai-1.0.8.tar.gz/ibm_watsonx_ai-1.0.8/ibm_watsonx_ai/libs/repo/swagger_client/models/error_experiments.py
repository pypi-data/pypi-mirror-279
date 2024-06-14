# coding: utf-8

#  -----------------------------------------------------------------------------------------
#  (C) Copyright IBM Corp. 2023-2024.
#  https://opensource.org/licenses/BSD-3-Clause
#  -----------------------------------------------------------------------------------------

from pprint import pformat
from six import iteritems
import re


class ErrorExperiments(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self, code=None, message=None, more_info=None, target=None):
        """
        ErrorExperiments - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'code': 'str',
            'message': 'str',
            'more_info': 'str',
            'target': 'ErrorExperimentsTarget'
        }

        self.attribute_map = {
            'code': 'code',
            'message': 'message',
            'more_info': 'more_info',
            'target': 'target'
        }

        self._code = code
        self._message = message
        self._more_info = more_info
        self._target = target

    @property
    def code(self):
        """
        Gets the code of this ErrorExperiments.


        :return: The code of this ErrorExperiments.
        :rtype: str
        """
        return self._code

    @code.setter
    def code(self, code):
        """
        Sets the code of this ErrorExperiments.


        :param code: The code of this ErrorExperiments.
        :type: str
        """

        self._code = code

    @property
    def message(self):
        """
        Gets the message of this ErrorExperiments.


        :return: The message of this ErrorExperiments.
        :rtype: str
        """
        return self._message

    @message.setter
    def message(self, message):
        """
        Sets the message of this ErrorExperiments.


        :param message: The message of this ErrorExperiments.
        :type: str
        """

        self._message = message

    @property
    def more_info(self):
        """
        Gets the more_info of this ErrorExperiments.


        :return: The more_info of this ErrorExperiments.
        :rtype: str
        """
        return self._more_info

    @more_info.setter
    def more_info(self, more_info):
        """
        Sets the more_info of this ErrorExperiments.


        :param more_info: The more_info of this ErrorExperiments.
        :type: str
        """

        self._more_info = more_info

    @property
    def target(self):
        """
        Gets the target of this ErrorExperiments.


        :return: The target of this ErrorExperiments.
        :rtype: ErrorExperimentsTarget
        """
        return self._target

    @target.setter
    def target(self, target):
        """
        Sets the target of this ErrorExperiments.


        :param target: The target of this ErrorExperiments.
        :type: ErrorExperimentsTarget
        """

        self._target = target

    def to_dict(self):
        """
        Returns the model properties as a dict
        """
        result = {}

        for attr, _ in iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_str(self):
        """
        Returns the string representation of the model
        """
        return pformat(self.to_dict())

    def __repr__(self):
        """
        For `print` and `pprint`
        """
        return self.to_str()

    def __eq__(self, other):
        """
        Returns true if both objects are equal
        """
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
