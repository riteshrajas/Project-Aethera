# Code for device control
from typing import Dict, Any, List, Optional


class Device:
    """
    Represents a generic connected device in the Aethera automation system.
    """

    def __init__(self, device_id: str, name: str, device_type: str):
        """
        Initializes a new Device instance.

        Args:
            device_id (str): A unique identifier for the device.
            name (str): The human-readable name of the device.
            device_type (str): The category or type of the device (e.g., 'light', 'fan').
        """
        self.device_id = device_id
        self.name = name
        self.device_type = device_type
        self.status: str = "off"
        self.metadata: Dict[str, Any] = {}

    def turn_on(self) -> None:
        """Sets the device status to 'on'."""
        self.status = "on"

    def turn_off(self) -> None:
        """Sets the device status to 'off'."""
        self.status = "off"

    def get_info(self) -> Dict[str, Any]:
        """
        Retrieves the current information and status of the device.

        Returns:
            Dict[str, Any]: A dictionary containing device details.
        """
        return {
            "device_id": self.device_id,
            "name": self.name,
            "type": self.device_type,
            "status": self.status,
            "metadata": self.metadata,
        }


class DeviceManager:
    """
    Manages a collection of devices, providing methods for registration,
    retrieval, and status monitoring.
    """

    def __init__(self):
        """Initializes a new DeviceManager instance."""
        self._devices: Dict[str, Device] = {}

    def register_device(self, device: Device) -> None:
        """
        Registers a device with the manager.

        Args:
            device (Device): The device instance to register.
        """
        self._devices[device.device_id] = device

    def unregister_device(self, device_id: str) -> None:
        """
        Removes a device from the manager.

        Args:
            device_id (str): The unique identifier of the device to remove.
        """
        if device_id in self._devices:
            del self._devices[device_id]

    def get_device(self, device_id: str) -> Optional[Device]:
        """
        Retrieves a registered device by its ID.

        Args:
            device_id (str): The unique identifier of the device.

        Returns:
            Optional[Device]: The device instance if found, otherwise None.
        """
        return self._devices.get(device_id)

    def list_devices(self) -> List[Device]:
        """
        Lists all devices currently registered with the manager.

        Returns:
            List[Device]: A list of Device instances.
        """
        return list(self._devices.values())

    def get_all_devices_status(self) -> List[Dict[str, Any]]:
        """
        Collects the status information for all registered devices.

        Returns:
            List[Dict[str, Any]]: A list of status dictionaries.
        """
        return [device.get_info() for device in self._devices.values()]
