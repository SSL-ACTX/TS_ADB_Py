import base64
import os
from flask import Flask, jsonify, send_file
import subprocess

app = Flask(__name__)


def run_adb_command(command):
    """Run the ADB command and return the output."""
    try:
        output = subprocess.check_output(command, shell=True, text=True)
        return output.strip()
    except subprocess.CalledProcessError as e:
        return f"Error: {e}"


@app.route('/adb/cpu', methods=['GET'])
def get_cpu_usage():
    """Get CPU usage statistics from ADB."""
    command = "adb shell top -m 10"
    output = run_adb_command(command)
    return jsonify({"cpu_usage": output})


@app.route('/adb/battery', methods=['GET'])
def get_battery_usage():
    """Get battery usage statistics from ADB."""
    command = "adb shell dumpsys battery"
    output = run_adb_command(command)
    return jsonify({"battery_usage": output})


@app.route('/adb/device_info', methods=['GET'])
def get_device_info():
    """Get device information from ADB."""
    command = "adb shell getprop"
    output = run_adb_command(command)
    return jsonify({"device_info": output})


@app.route('/adb/memory', methods=['GET'])
def get_memory_usage():
    """Get memory usage statistics from ADB."""
    command = "adb shell dumpsys meminfo"
    output = run_adb_command(command)
    return jsonify({"memory_usage": output})


@app.route('/adb/packages', methods=['GET'])
def get_installed_packages():
    """Get a list of installed packages from ADB."""
    command = "adb shell pm list packages"
    output = run_adb_command(command)
    packages = output.splitlines() if isinstance(output, str) else []
    return jsonify({"installed_packages": packages})


@app.route('/adb/model', methods=['GET'])
def get_device_model():
    """Get device model and Android version."""
    model_command = "adb shell getprop ro.product.model"
    version_command = "adb shell getprop ro.build.version.release"
    model = run_adb_command(model_command)
    version = run_adb_command(version_command)
    return jsonify({"model": model, "android_version": version})


@app.route('/adb/network', methods=['GET'])
def get_network_info():
    """Get network information from ADB."""
    command = "adb shell ip addr show"
    output = run_adb_command(command)
    return jsonify({"network_info": output})


@app.route('/adb/storage', methods=['GET'])
def get_storage_info():
    """Get storage information from ADB."""
    command = "adb shell df -h"
    output = run_adb_command(command)
    return jsonify({"storage_info": output})


@app.route('/adb/logcat', methods=['GET'])
def get_logcat():
    """Get the logcat output from ADB."""
    command = "adb logcat -d"
    output = run_adb_command(command)
    return jsonify({"logcat": output})


@app.route('/adb/sensors', methods=['GET'])
def get_sensor_info():
    """Get sensor information from ADB."""
    command = "adb shell dumpsys sensorservice"
    output = run_adb_command(command)
    return jsonify({"sensors": output})


@app.route('/adb/running_apps', methods=['GET'])
def get_running_apps():
    """Get a list of currently running apps from ADB."""
    command = "adb shell dumpsys activity"
    output = run_adb_command(command)
    return jsonify({"running_apps": output})


@app.route('/adb/version', methods=['GET'])
def get_adb_version():
    """Get the ADB version."""
    command = "adb version"
    output = run_adb_command(command)
    return jsonify({"adb_version": output})


@app.route('/adb/services', methods=['GET'])
def get_running_services():
    """Get a list of running services from ADB."""
    command = "adb shell dumpsys activity services"
    output = run_adb_command(command)
    return jsonify({"running_services": output})


@app.route('/adb/wifi_status', methods=['GET'])
def get_wifi_status():
    """Get the Wi-Fi connection status."""
    command = "adb shell dumpsys wifi"
    output = run_adb_command(command)
    return jsonify({"wifi_status": output})


@app.route('/adb/connected_devices', methods=['GET'])
def get_connected_devices():
    """Get a list of connected USB devices."""
    command = "adb devices"
    output = run_adb_command(command)
    connected_devices = output.splitlines() if isinstance(output, str) else []
    return jsonify({"connected_devices": connected_devices})


@app.route('/adb/packages_info', methods=['GET'])
def get_packages_info():
    """Get detailed information about all installed packages."""
    command = "adb shell pm list packages -f"
    output = run_adb_command(command)
    packages_info = output.splitlines() if isinstance(output, str) else []
    return jsonify({"packages_info": packages_info})


@app.route('/adb/uptime', methods=['GET'])
def get_uptime():
    """Get the uptime of the device."""
    command = "adb shell uptime"
    output = run_adb_command(command)
    return jsonify({"uptime": output})


@app.route('/adb/app_permissions/<package_name>', methods=['GET'])
def get_app_permissions(package_name):
    """Get permissions granted to a specific app."""
    command = f"adb shell dumpsys package {package_name} | grep 'permission'"
    output = run_adb_command(command)
    return jsonify({"app_permissions": output})


@app.route('/adb/screenshot', methods=['GET'])
def take_screenshot():
    """Take a screenshot and return the image data."""
    # Take the screenshot and save it as a temporary file
    temp_file_path = "screenshot.png"
    command = f"adb exec-out screencap -p > {temp_file_path}"
    run_adb_command(command)

    # Read the image file and encode it in base64
    with open(temp_file_path, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode('utf-8')

    # Optionally, remove the temporary file after reading
    os.remove(temp_file_path)

    # Return the base64 image data
    return jsonify({"screenshot": encoded_image})


@app.route('/adb/reboot', methods=['POST'])
def reboot_device():
    """Reboot the connected device."""
    command = "adb reboot"
    output = run_adb_command(command)
    return jsonify({"reboot_status": output})


@app.route('/adb/logcat_clear', methods=['POST'])
def clear_logcat():
    """Clear the logcat buffer."""
    command = "adb logcat -c"
    output = run_adb_command(command)
    return jsonify({"clear_logcat_status": "Logcat buffer cleared"})


@app.route('/adb/bt_status', methods=['GET'])
def get_bluetooth_info():
    """Get Bluetooth status information."""
    command = "adb shell dumpsys bluetooth_manager"
    output = run_adb_command(command)
    return jsonify({"bluetooth_info": output})


@app.route('/adb/location', methods=['GET'])
def get_location_info():
    """Get device location services status."""
    command = "adb shell dumpsys location"
    output = run_adb_command(command)
    return jsonify({"location_info": output})


@app.route('/adb/installed_apps', methods=['GET'])
def get_installed_apps():
    """Get a list of all installed apps with details."""
    command = "adb shell pm list packages -f"
    output = run_adb_command(command)
    installed_apps = output.splitlines() if isinstance(output, str) else []
    return jsonify({"installed_apps": installed_apps})


@app.route('/adb/set_property/<property_name>/<value>', methods=['POST'])
def set_property(property_name, value):
    """Set a system property on the device."""
    command = f"adb shell setprop {property_name} {value}"
    output = run_adb_command(command)
    return jsonify({"set_property_status": output})


@app.route('/adb/usage_stats', methods=['GET'])
def get_usage_stats():
    """Get app usage statistics."""
    command = "adb shell dumpsys usagestats"
    output = run_adb_command(command)
    return jsonify({"usage_stats": output})


@app.route('/adb/brightness', methods=['GET'])
def get_brightness():
    """Get the current screen brightness level."""
    command = "adb shell settings get system screen_brightness"
    output = run_adb_command(command)
    return jsonify({"brightness": output})


@app.route('/adb/set_brightness/<int:value>', methods=['POST'])
def set_brightness(value):
    """Set the screen brightness level (0-255)."""
    command = f"adb shell settings put system screen_brightness {value}"
    output = run_adb_command(command)
    return jsonify({"set_brightness_status": output})


@app.route('/adb/airplane_mode', methods=['GET'])
def get_airplane_mode():
    """Get the airplane mode status."""
    command = "adb shell settings get global airplane_mode_on"
    output = run_adb_command(command)
    return jsonify({"airplane_mode": output})


@app.route('/adb/set_airplane_mode/<int:value>', methods=['POST'])
def set_airplane_mode(value):
    """Enable or disable airplane mode."""
    command = f"adb shell settings put global airplane_mode_on {value}"
    run_adb_command(command)
    # Broadcast the change
    command = "adb shell am broadcast -a android.intent.action.AIRPLANE_MODE --ez state " + \
        str(bool(value)).lower()
    run_adb_command(command)
    return jsonify({"set_airplane_mode_status": "Airplane mode set to " + str(bool(value))})


@app.route('/adb/notifications', methods=['GET'])
def get_notifications():
    """Get the current notifications on the device."""
    command = "adb shell dumpsys notification"
    output = run_adb_command(command)
    return jsonify({"notifications": output})


@app.route('/adb/kill_app/<package_name>', methods=['POST'])
def kill_app(package_name):
    """Kill a running app by its package name."""
    command = f"adb shell am force-stop {package_name}"
    output = run_adb_command(command)
    return jsonify({"kill_app_status": f"Killed app {package_name}"})


@app.route('/adb/install_app', methods=['POST'])
def install_app():
    """Install an APK from the local machine to the connected device."""
    # The APK path should be provided in the request body
    apk_path = request.json.get('apk_path')
    command = f"adb install {apk_path}"
    output = run_adb_command(command)
    return jsonify({"install_status": output})


@app.route('/adb/uninstall_app/<package_name>', methods=['POST'])
def uninstall_app(package_name):
    """Uninstall an app by its package name."""
    command = f"adb uninstall {package_name}"
    output = run_adb_command(command)
    return jsonify({"uninstall_status": output})


@app.route('/adb/media_volume', methods=['GET'])
def get_media_volume():
    """Get the current media volume level."""
    command = "adb shell media volume --get"
    output = run_adb_command(command)
    return jsonify({"media_volume": output})


@app.route('/adb/set_media_volume/<int:value>', methods=['POST'])
def set_media_volume(value):
    """Set the media volume level (0-15)."""
    command = f"adb shell media volume --set {value}"
    output = run_adb_command(command)
    return jsonify({"set_media_volume_status": output})


@app.route('/adb/foreground_activity', methods=['GET'])
def get_foreground_activity():
    """Get the currently foreground app."""
    command = "adb shell dumpsys activity | grep 'mResumedActivity'"
    output = run_adb_command(command)
    return jsonify({"foreground_activity": output})


@app.route('/adb/clear_app_data/<package_name>', methods=['POST'])
def clear_app_data(package_name):
    """Clear data for a specific app by package name."""
    command = f"adb shell pm clear {package_name}"
    output = run_adb_command(command)
    return jsonify({"clear_app_data_status": f"Cleared data for {package_name}"})


@app.route('/adb/clear_cache', methods=['POST'])
def clear_cache():
    """Clear the cache for all apps."""
    command = "adb shell pm trim-caches 9999999999"
    output = run_adb_command(command)
    return jsonify({"clear_cache_status": output})


@app.route('/adb/device_ip', methods=['GET'])
def get_device_ip():
    """Get the device's IP address."""
    command = "adb shell ip route | awk '{print $9}'"
    output = run_adb_command(command)
    return jsonify({"device_ip": output})


@app.route('/adb/system_time', methods=['GET'])
def get_system_time():
    """Get the current system time on the device."""
    command = "adb shell date"
    output = run_adb_command(command)
    return jsonify({"system_time": output})


@app.route('/adb/net_info', methods=['GET'])
def get_net_info():
    """Get the current network information."""
    command = "adb shell dumpsys connectivity"
    output = run_adb_command(command)
    return jsonify({"network_info": output})


if __name__ == '__main__':
    app.run(debug=True)
