import pytest
from core.automation.devices import Device, DeviceManager

def test_device_initialization():
    device = Device("light-1", "Living Room Light", "light")
    assert device.device_id == "light-1"
    assert device.name == "Living Room Light"
    assert device.device_type == "light"
    assert device.status == "off"
    assert device.metadata == {}

def test_device_turn_on_off():
    device = Device("light-1", "Living Room Light", "light")
    device.turn_on()
    assert device.status == "on"
    device.turn_off()
    assert device.status == "off"

def test_device_get_info():
    device = Device("light-1", "Living Room Light", "light")
    info = device.get_info()
    assert info["device_id"] == "light-1"
    assert info["status"] == "off"

def test_device_manager_register_and_get():
    manager = DeviceManager()
    device = Device("light-1", "Living Room Light", "light")
    manager.register_device(device)

    assert manager.get_device("light-1") == device
    assert len(manager.list_devices()) == 1
    assert manager.list_devices()[0] == device

def test_device_manager_unregister():
    manager = DeviceManager()
    device = Device("light-1", "Living Room Light", "light")
    manager.register_device(device)
    manager.unregister_device("light-1")

    assert manager.get_device("light-1") is None
    assert len(manager.list_devices()) == 0

def test_device_manager_get_all_status():
    manager = DeviceManager()
    device1 = Device("light-1", "Living Room Light", "light")
    device2 = Device("fan-1", "Office Fan", "fan")
    manager.register_device(device1)
    manager.register_device(device2)

    statuses = manager.get_all_devices_status()
    assert len(statuses) == 2
    ids = [s["device_id"] for s in statuses]
    assert "light-1" in ids
    assert "fan-1" in ids
