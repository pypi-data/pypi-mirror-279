# coding: utf-8

"""
    AssistedInstall

    Assisted installation  # noqa: E501

    OpenAPI spec version: 1.0.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six


class Disk(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'id': 'str',
        'drive_type': 'DriveType',
        'has_uuid': 'bool',
        'vendor': 'str',
        'name': 'str',
        'path': 'str',
        'hctl': 'str',
        'by_path': 'str',
        'by_id': 'str',
        'model': 'str',
        'wwn': 'str',
        'serial': 'str',
        'size_bytes': 'int',
        'bootable': 'bool',
        'removable': 'bool',
        'partition_types': 'str',
        'is_installation_media': 'bool',
        'installation_eligibility': 'DiskInstallationEligibility',
        'smart': 'str',
        'io_perf': 'IoPerf',
        'holders': 'str'
    }

    attribute_map = {
        'id': 'id',
        'drive_type': 'drive_type',
        'has_uuid': 'has_uuid',
        'vendor': 'vendor',
        'name': 'name',
        'path': 'path',
        'hctl': 'hctl',
        'by_path': 'by_path',
        'by_id': 'by_id',
        'model': 'model',
        'wwn': 'wwn',
        'serial': 'serial',
        'size_bytes': 'size_bytes',
        'bootable': 'bootable',
        'removable': 'removable',
        'partition_types': 'partitionTypes',
        'is_installation_media': 'is_installation_media',
        'installation_eligibility': 'installation_eligibility',
        'smart': 'smart',
        'io_perf': 'io_perf',
        'holders': 'holders'
    }

    def __init__(self, id=None, drive_type=None, has_uuid=None, vendor=None, name=None, path=None, hctl=None, by_path=None, by_id=None, model=None, wwn=None, serial=None, size_bytes=None, bootable=None, removable=None, partition_types=None, is_installation_media=None, installation_eligibility=None, smart=None, io_perf=None, holders=None):  # noqa: E501
        """Disk - a model defined in Swagger"""  # noqa: E501

        self._id = None
        self._drive_type = None
        self._has_uuid = None
        self._vendor = None
        self._name = None
        self._path = None
        self._hctl = None
        self._by_path = None
        self._by_id = None
        self._model = None
        self._wwn = None
        self._serial = None
        self._size_bytes = None
        self._bootable = None
        self._removable = None
        self._partition_types = None
        self._is_installation_media = None
        self._installation_eligibility = None
        self._smart = None
        self._io_perf = None
        self._holders = None
        self.discriminator = None

        if id is not None:
            self.id = id
        if drive_type is not None:
            self.drive_type = drive_type
        if has_uuid is not None:
            self.has_uuid = has_uuid
        if vendor is not None:
            self.vendor = vendor
        if name is not None:
            self.name = name
        if path is not None:
            self.path = path
        if hctl is not None:
            self.hctl = hctl
        if by_path is not None:
            self.by_path = by_path
        if by_id is not None:
            self.by_id = by_id
        if model is not None:
            self.model = model
        if wwn is not None:
            self.wwn = wwn
        if serial is not None:
            self.serial = serial
        if size_bytes is not None:
            self.size_bytes = size_bytes
        if bootable is not None:
            self.bootable = bootable
        if removable is not None:
            self.removable = removable
        if partition_types is not None:
            self.partition_types = partition_types
        if is_installation_media is not None:
            self.is_installation_media = is_installation_media
        if installation_eligibility is not None:
            self.installation_eligibility = installation_eligibility
        if smart is not None:
            self.smart = smart
        if io_perf is not None:
            self.io_perf = io_perf
        if holders is not None:
            self.holders = holders

    @property
    def id(self):
        """Gets the id of this Disk.  # noqa: E501

        Determine the disk's unique identifier which is the by-id field if it exists and fallback to the by-path field otherwise  # noqa: E501

        :return: The id of this Disk.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this Disk.

        Determine the disk's unique identifier which is the by-id field if it exists and fallback to the by-path field otherwise  # noqa: E501

        :param id: The id of this Disk.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def drive_type(self):
        """Gets the drive_type of this Disk.  # noqa: E501


        :return: The drive_type of this Disk.  # noqa: E501
        :rtype: DriveType
        """
        return self._drive_type

    @drive_type.setter
    def drive_type(self, drive_type):
        """Sets the drive_type of this Disk.


        :param drive_type: The drive_type of this Disk.  # noqa: E501
        :type: DriveType
        """

        self._drive_type = drive_type

    @property
    def has_uuid(self):
        """Gets the has_uuid of this Disk.  # noqa: E501


        :return: The has_uuid of this Disk.  # noqa: E501
        :rtype: bool
        """
        return self._has_uuid

    @has_uuid.setter
    def has_uuid(self, has_uuid):
        """Sets the has_uuid of this Disk.


        :param has_uuid: The has_uuid of this Disk.  # noqa: E501
        :type: bool
        """

        self._has_uuid = has_uuid

    @property
    def vendor(self):
        """Gets the vendor of this Disk.  # noqa: E501


        :return: The vendor of this Disk.  # noqa: E501
        :rtype: str
        """
        return self._vendor

    @vendor.setter
    def vendor(self, vendor):
        """Sets the vendor of this Disk.


        :param vendor: The vendor of this Disk.  # noqa: E501
        :type: str
        """

        self._vendor = vendor

    @property
    def name(self):
        """Gets the name of this Disk.  # noqa: E501


        :return: The name of this Disk.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this Disk.


        :param name: The name of this Disk.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def path(self):
        """Gets the path of this Disk.  # noqa: E501


        :return: The path of this Disk.  # noqa: E501
        :rtype: str
        """
        return self._path

    @path.setter
    def path(self, path):
        """Sets the path of this Disk.


        :param path: The path of this Disk.  # noqa: E501
        :type: str
        """

        self._path = path

    @property
    def hctl(self):
        """Gets the hctl of this Disk.  # noqa: E501


        :return: The hctl of this Disk.  # noqa: E501
        :rtype: str
        """
        return self._hctl

    @hctl.setter
    def hctl(self, hctl):
        """Sets the hctl of this Disk.


        :param hctl: The hctl of this Disk.  # noqa: E501
        :type: str
        """

        self._hctl = hctl

    @property
    def by_path(self):
        """Gets the by_path of this Disk.  # noqa: E501

        by-path is the shortest physical path to the device  # noqa: E501

        :return: The by_path of this Disk.  # noqa: E501
        :rtype: str
        """
        return self._by_path

    @by_path.setter
    def by_path(self, by_path):
        """Sets the by_path of this Disk.

        by-path is the shortest physical path to the device  # noqa: E501

        :param by_path: The by_path of this Disk.  # noqa: E501
        :type: str
        """

        self._by_path = by_path

    @property
    def by_id(self):
        """Gets the by_id of this Disk.  # noqa: E501

        by-id is the World Wide Number of the device which guaranteed to be unique for every storage device  # noqa: E501

        :return: The by_id of this Disk.  # noqa: E501
        :rtype: str
        """
        return self._by_id

    @by_id.setter
    def by_id(self, by_id):
        """Sets the by_id of this Disk.

        by-id is the World Wide Number of the device which guaranteed to be unique for every storage device  # noqa: E501

        :param by_id: The by_id of this Disk.  # noqa: E501
        :type: str
        """

        self._by_id = by_id

    @property
    def model(self):
        """Gets the model of this Disk.  # noqa: E501


        :return: The model of this Disk.  # noqa: E501
        :rtype: str
        """
        return self._model

    @model.setter
    def model(self, model):
        """Sets the model of this Disk.


        :param model: The model of this Disk.  # noqa: E501
        :type: str
        """

        self._model = model

    @property
    def wwn(self):
        """Gets the wwn of this Disk.  # noqa: E501


        :return: The wwn of this Disk.  # noqa: E501
        :rtype: str
        """
        return self._wwn

    @wwn.setter
    def wwn(self, wwn):
        """Sets the wwn of this Disk.


        :param wwn: The wwn of this Disk.  # noqa: E501
        :type: str
        """

        self._wwn = wwn

    @property
    def serial(self):
        """Gets the serial of this Disk.  # noqa: E501


        :return: The serial of this Disk.  # noqa: E501
        :rtype: str
        """
        return self._serial

    @serial.setter
    def serial(self, serial):
        """Sets the serial of this Disk.


        :param serial: The serial of this Disk.  # noqa: E501
        :type: str
        """

        self._serial = serial

    @property
    def size_bytes(self):
        """Gets the size_bytes of this Disk.  # noqa: E501


        :return: The size_bytes of this Disk.  # noqa: E501
        :rtype: int
        """
        return self._size_bytes

    @size_bytes.setter
    def size_bytes(self, size_bytes):
        """Sets the size_bytes of this Disk.


        :param size_bytes: The size_bytes of this Disk.  # noqa: E501
        :type: int
        """

        self._size_bytes = size_bytes

    @property
    def bootable(self):
        """Gets the bootable of this Disk.  # noqa: E501


        :return: The bootable of this Disk.  # noqa: E501
        :rtype: bool
        """
        return self._bootable

    @bootable.setter
    def bootable(self, bootable):
        """Sets the bootable of this Disk.


        :param bootable: The bootable of this Disk.  # noqa: E501
        :type: bool
        """

        self._bootable = bootable

    @property
    def removable(self):
        """Gets the removable of this Disk.  # noqa: E501


        :return: The removable of this Disk.  # noqa: E501
        :rtype: bool
        """
        return self._removable

    @removable.setter
    def removable(self, removable):
        """Sets the removable of this Disk.


        :param removable: The removable of this Disk.  # noqa: E501
        :type: bool
        """

        self._removable = removable

    @property
    def partition_types(self):
        """Gets the partition_types of this Disk.  # noqa: E501


        :return: The partition_types of this Disk.  # noqa: E501
        :rtype: str
        """
        return self._partition_types

    @partition_types.setter
    def partition_types(self, partition_types):
        """Sets the partition_types of this Disk.


        :param partition_types: The partition_types of this Disk.  # noqa: E501
        :type: str
        """

        self._partition_types = partition_types

    @property
    def is_installation_media(self):
        """Gets the is_installation_media of this Disk.  # noqa: E501

        Whether the disk appears to be an installation media or not  # noqa: E501

        :return: The is_installation_media of this Disk.  # noqa: E501
        :rtype: bool
        """
        return self._is_installation_media

    @is_installation_media.setter
    def is_installation_media(self, is_installation_media):
        """Sets the is_installation_media of this Disk.

        Whether the disk appears to be an installation media or not  # noqa: E501

        :param is_installation_media: The is_installation_media of this Disk.  # noqa: E501
        :type: bool
        """

        self._is_installation_media = is_installation_media

    @property
    def installation_eligibility(self):
        """Gets the installation_eligibility of this Disk.  # noqa: E501


        :return: The installation_eligibility of this Disk.  # noqa: E501
        :rtype: DiskInstallationEligibility
        """
        return self._installation_eligibility

    @installation_eligibility.setter
    def installation_eligibility(self, installation_eligibility):
        """Sets the installation_eligibility of this Disk.


        :param installation_eligibility: The installation_eligibility of this Disk.  # noqa: E501
        :type: DiskInstallationEligibility
        """

        self._installation_eligibility = installation_eligibility

    @property
    def smart(self):
        """Gets the smart of this Disk.  # noqa: E501


        :return: The smart of this Disk.  # noqa: E501
        :rtype: str
        """
        return self._smart

    @smart.setter
    def smart(self, smart):
        """Sets the smart of this Disk.


        :param smart: The smart of this Disk.  # noqa: E501
        :type: str
        """

        self._smart = smart

    @property
    def io_perf(self):
        """Gets the io_perf of this Disk.  # noqa: E501


        :return: The io_perf of this Disk.  # noqa: E501
        :rtype: IoPerf
        """
        return self._io_perf

    @io_perf.setter
    def io_perf(self, io_perf):
        """Sets the io_perf of this Disk.


        :param io_perf: The io_perf of this Disk.  # noqa: E501
        :type: IoPerf
        """

        self._io_perf = io_perf

    @property
    def holders(self):
        """Gets the holders of this Disk.  # noqa: E501

        A comma-separated list of disk names that this disk belongs to  # noqa: E501

        :return: The holders of this Disk.  # noqa: E501
        :rtype: str
        """
        return self._holders

    @holders.setter
    def holders(self, holders):
        """Sets the holders of this Disk.

        A comma-separated list of disk names that this disk belongs to  # noqa: E501

        :param holders: The holders of this Disk.  # noqa: E501
        :type: str
        """

        self._holders = holders

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
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
        if issubclass(Disk, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, Disk):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
