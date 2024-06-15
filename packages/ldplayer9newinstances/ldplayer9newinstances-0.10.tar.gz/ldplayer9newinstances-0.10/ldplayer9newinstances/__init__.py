from list_all_files_recursively_short import (
    get_folder_file_complete_path,
    get_short_path_name,
)
import subprocess
import os
import shutil
import json
import re
from flatten_everything import flatten_everything
import random
from flatten_any_dict_iterable_or_whatsoever import (
    fla_tu,
    set_in_original_iter,
)
import xmltodict

regex_for_uuid = re.compile(
    r"[a-z0-9]{8}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{12}",
    flags=re.IGNORECASE,
)
startupinfo = subprocess.STARTUPINFO()
startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
startupinfo.wShowWindow = subprocess.SW_HIDE
creationflags = subprocess.CREATE_NO_WINDOW
invisibledict = {
    "startupinfo": startupinfo,
    "creationflags": creationflags,
    "start_new_session": True,
}


def create_independent_instance(
    basic_config: dict,
    vboxmanage_path: str = r"C:\Program Files\Oracle\VirtualBox\VBoxManage.exe",
    ldplayer_folder: str = r"C:\LDPlayer",
) -> str:
    """
    Creates an independent instance of LDPlayer9 instances using

    Args:
        basic_config (dict): The basic configuration for the virtual machine.
        vboxmanage_path (str, optional): The path to the VBoxManage executable. Defaults to r"C:\Program Files\Oracle\VirtualBox\VBoxManage.exe".
        ldplayer_folder (str, optional): The path to the LDPlayer folder. Defaults to r"C:\LDPlayer".

    Returns:
        str: The path to the newly created virtual machine folder.

    Raises:
        None

    Description:
        This function creates an independent instance of a virtual machine using the specified basic configuration.
        It first retrieves the necessary paths and files using the provided ldplayer_folder parameter.
        It then calls the get_highest_current_index_number function to determine the highest current index number.
        Next, it creates a new folder with a unique name based on the highest index number.
        It copies the system.vmdk, data.vmdk, and sdcard.vmdk files from the original LDPlayer folder to the new folder.
        It retrieves the short paths for the copied files using the get_short_path_name function.
        It generates new UUIDs for the system disk, data disk, new machine, and sdcard using the next index number.
        It creates a new_emulator_data dictionary containing the generated UUIDs and other information.
        It updates the UUIDs of the copied files using the VBoxManage command.
    Example:
        from ldplayer9newinstances import create_independent_instance
        import random
        basic_configuration = {
            "propertySettings.phoneIMEI": "351542017956834",
            "propertySettings.phoneIMSI": "460003931985310",
            "propertySettings.phoneSimSerial": "89861050793589253274",
            "propertySettings.phoneAndroidId": "5da5e11ca1b514d6",
            "propertySettings.phoneModel": "ASUS_Z01QD",
            "propertySettings.phoneManufacturer": "asus",
            "propertySettings.macAddress": (
                "%02x%02x%02x%02x%02x%02x" % tuple(random.randint(0, 255) for v in range(6))
            ).upper(),
            "statusSettings.playerName": "",
            "basicSettings.verticalSync": False,
            "basicSettings.fsAutoSize": 1,
            "basicSettings.autoRun": False,
            "basicSettings.rootMode": True,
            "statusSettings.closeOption": 0,
            "basicSettings.heightFrameRate": False,
            "basicSettings.adbDebug": 1,
            "advancedSettings.resolution": {"width": 1280, "height": 720},
            "advancedSettings.resolutionDpi": 240,
            "advancedSettings.cpuCount": 4,
            "advancedSettings.memorySize": 4096,
            "propertySettings.phoneNumber": "",
            "basicSettings.autoRotate": False,
            "basicSettings.isForceLandscape": False,
            "basicSettings.standaloneSysVmdk": True,
            "basicSettings.lockWindow": False,
            "advancedSettings.micphoneName": "",
            "advancedSettings.speakerName": "",
            "networkSettings.networkEnable": True,
            "networkSettings.networkSwitching": False,
            "networkSettings.networkStatic": False,
            "networkSettings.networkAddress": "0.0.0.0",
            "networkSettings.networkGateway": "0.0.0.0",
            "networkSettings.networkSubnetMask": "255.255.255.0",
            "networkSettings.networkDNS1": "8.8.8.8",
            "networkSettings.networkDNS2": "8.8.4.4",
            "networkSettings.networkInterface": "",
            "basicSettings.disableMouseFastOpt": True,
            "basicSettings.cjztdisableMouseFastOpt_new": 0,
            "basicSettings.HDRQuality": 0,
            "basicSettings.qjcjdisableMouseFast": 1,
            "basicSettings.fps": 60,
            "basicSettings.astc": True,
            "hotkeySettings.backKey": {"modifiers": 0, "key": 27},
            "hotkeySettings.homeKey": {"modifiers": 0, "key": 112},
            "hotkeySettings.appSwitchKey": {"modifiers": 0, "key": 113},
            "hotkeySettings.menuKey": {"modifiers": 0, "key": 114},
            "hotkeySettings.zoomInKey": {"modifiers": 0, "key": 115},
            "hotkeySettings.zoomOutKey": {"modifiers": 0, "key": 116},
            "hotkeySettings.bossKey": {"modifiers": 2, "key": 81},
            "hotkeySettings.shakeKey": {"modifiers": 0, "key": 120},
            "hotkeySettings.operationRecordKey": {"modifiers": 0, "key": 121},
            "hotkeySettings.operationRecordPauseKey": {"modifiers": 0, "key": 0},
            "hotkeySettings.operationRecordShowFrame": {"modifiers": 2, "key": 56},
            "hotkeySettings.fullScreenKey": {"modifiers": 0, "key": 122},
            "hotkeySettings.showMappingKey": {"modifiers": 0, "key": 123},
            "hotkeySettings.videoRecordKey": {"modifiers": 0, "key": 119},
            "hotkeySettings.mappingRecordKey": {"modifiers": 0, "key": 117},
            "hotkeySettings.keyboardModelKey": {"modifiers": 2, "key": 70},
        }
        newfolder = create_independent_instance(
            basic_config=basic_configuration,
            vboxmanage_path=r"C:\Program Files\Oracle\VirtualBox\VBoxManage.exe",
            ldplayer_folder=r"C:\LDPlayer",
        )
        print(newfolder)

    """
    VBOXMANAGE_PATH_SHORT = get_short_path_name(vboxmanage_path)
    ldplayer_files = get_folder_file_complete_path(ldplayer_folder)
    original_system_disk = os.path.join(ldplayer_folder, "LDPlayer9", "system.vmdk")
    original_sd_and_data = os.path.join(ldplayer_folder, "LDPlayer9", "data.vmdk")
    PREFIX_FOR_NEW_FOLDER = os.path.join(ldplayer_folder, "LDPlayer9", "vms", "leidian")
    JSON_CFG_FOLDER = os.path.join(ldplayer_folder, "LDPlayer9", "vms", "config")

    def get_highest_current_index_number():
        all_uuids = []
        for f in ldplayer_files:
            if f.ext.lower() == ".vmdk":
                all_uuids.append(f._asdict())
                pr = subprocess.run(
                    [VBOXMANAGE_PATH_SHORT, "showhdinfo", f.name83],
                    capture_output=True,
                    **invisibledict,
                )
                all_uuids[-1]["stdout"] = pr.stdout.decode("utf-8", errors="ignore")
                all_uuids[-1]["stderr"] = pr.stderr.decode("utf-8", errors="ignore")

        uuids_split = list(
            flatten_everything(
                [regex_for_uuid.findall(str(l["stdout"])) for l in all_uuids]
            )
        )
        biggest_number = [
            x.strip().split("-")[-1].lstrip("0") for x in set(uuids_split)
        ]
        biggest_number = [
            int(x, 16) for x in biggest_number if len(x) < 5 and len(x) > 0
        ]
        return max(biggest_number), all_uuids, biggest_number

    lastindexnumber, all_uuids, all_converted_hexnumbers = (
        get_highest_current_index_number()
    )
    nextindexnumber = lastindexnumber + 1
    nextindexnumber_in_hex = hex(nextindexnumber).lower().replace("x", "").zfill(12)
    new_Folder = rf"{PREFIX_FOR_NEW_FOLDER}{nextindexnumber}"
    new_name_for_config = new_Folder.split(os.sep)[-1]
    new_name_json_config = os.path.join(
        JSON_CFG_FOLDER, f"leidian{nextindexnumber}.config"
    )
    new_vbox_file = os.path.join(new_Folder, "leidian.vbox")
    os.makedirs(new_Folder, exist_ok=True)
    systemdisk = os.path.join(new_Folder, "system.vmdk")
    datadisk = os.path.join(new_Folder, "data.vmdk")
    sdcardpath = os.path.join(new_Folder, "sdcard.vmdk")

    shutil.copyfile(original_system_disk, systemdisk)
    shutil.copyfile(original_sd_and_data, datadisk)
    shutil.copyfile(original_sd_and_data, sdcardpath)

    shortpath_systemdisk = get_short_path_name(systemdisk)
    shortpath_datadisk = get_short_path_name(datadisk)
    shortpath_sdcardpath = get_short_path_name(sdcardpath)

    systemdiskuuid = f"20160302-bbbb-bbbb-0eee-{nextindexnumber_in_hex}"
    datadiskuuid = f"20160302-cccc-cccc-0eee-{nextindexnumber_in_hex}"
    new_machine_uuid = f"20160302-aaaa-aaaa-0eee-{nextindexnumber_in_hex}"
    sdcarduuid = f"20160302-dddd-dddd-0eee-{nextindexnumber_in_hex}"

    new_emulator_data = {
        "next_index_int": nextindexnumber,
        "next_index_hex": nextindexnumber_in_hex,
        "uuid_system": systemdiskuuid,
        "uuid_data": datadiskuuid,
        "uuid_machine": new_machine_uuid,
        "uuid_sdcard": sdcarduuid,
    }
    for disk, disk_long, new_uuid, dictkey in zip(
        [shortpath_systemdisk, shortpath_datadisk, shortpath_sdcardpath],
        [systemdisk, datadisk, sdcardpath],
        [systemdiskuuid, datadiskuuid, sdcarduuid],
        ["disk_short", "disk_long", "disk_uuid"],
    ):
        proc = subprocess.run(
            [VBOXMANAGE_PATH_SHORT, "internalcommands", "sethduuid", disk, new_uuid],
            capture_output=True,
            **invisibledict,
        )
        new_emulator_data[dictkey] = {
            "stdout": proc.stdout.decode("utf-8", errors="ignore"),
            "stderr": proc.stderr.decode("utf-8", errors="ignore"),
            "returncode": proc.returncode,
        }

    all_vbox_files = sorted(
        [
            x
            for x in get_folder_file_complete_path(ldplayer_folder)
            if x.ext.lower() == ".vbox"
        ],
        key=lambda x: x.folder,
        reverse=True,
    )
    for xmlfile in all_vbox_files:
        with open(xmlfile.path, "r", encoding="utf-8") as f:
            data = f.read()
            resultsfound = len(
                re.findall(
                    r"HardDisk\s*uuid=.*?location.*?format.*?type",
                    data,
                )
            )
            if (resultsfound) == 1:
                dxml = xmltodict.parse(data)
                break

    for v, k in tuple(fla_tu(dxml)):
        if k == ("VirtualBox", "Machine", "@uuid"):
            set_in_original_iter(dxml, k, "{" + new_emulator_data["uuid_machine"] + "}")
        elif (
            k[-1] == "@uuid"
            and k[:2] == ("VirtualBox", "Machine")
            and ("HardDisk" in k or "HardDisks" in k)
        ) or (
            k[-1] == "@uuid"
            and k[:3]
            == (
                "VirtualBox",
                "Machine",
                "StorageControllers",
            )
        ):
            set_in_original_iter(dxml, k, "{" + new_emulator_data["uuid_data"] + "}")
        elif (
            k[-1] == "@MACAddress"
            and "Network" in k
            and "Adapter" in k
            and re.search(r"[0-9a-f]{12}", str(v), flags=re.IGNORECASE)
        ):
            set_in_original_iter(dxml, k, basic_config["propertySettings.macAddress"])
        elif k == ("VirtualBox", "Machine", "@name"):
            set_in_original_iter(dxml, k, new_name_for_config)

    with open(new_vbox_file, "w", encoding="utf-8") as f:
        f.write(xmltodict.unparse(dxml, pretty=True))

    with open(new_name_json_config, "w", encoding="utf-8") as f:
        f.write(json.dumps(basic_config, indent=4, ensure_ascii=False))
    return new_Folder


if __name__ == "__main__":
    # from ldplayer9newinstances import create_independent_instance

    basic_configuration = {
        "propertySettings.phoneIMEI": "351542017956834",
        "propertySettings.phoneIMSI": "460003931985310",
        "propertySettings.phoneSimSerial": "89861050793589253274",
        "propertySettings.phoneAndroidId": "5da5e11ca1b514d6",
        "propertySettings.phoneModel": "ASUS_Z01QD",
        "propertySettings.phoneManufacturer": "asus",
        "propertySettings.macAddress": (
            "%02x%02x%02x%02x%02x%02x" % tuple(random.randint(0, 255) for v in range(6))
        ).upper(),
        "statusSettings.playerName": "",
        "basicSettings.verticalSync": False,
        "basicSettings.fsAutoSize": 1,
        "basicSettings.autoRun": False,
        "basicSettings.rootMode": True,
        "statusSettings.closeOption": 0,
        "basicSettings.heightFrameRate": False,
        "basicSettings.adbDebug": 1,
        "advancedSettings.resolution": {"width": 1280, "height": 720},
        "advancedSettings.resolutionDpi": 240,
        "advancedSettings.cpuCount": 4,
        "advancedSettings.memorySize": 4096,
        "propertySettings.phoneNumber": "",
        "basicSettings.autoRotate": False,
        "basicSettings.isForceLandscape": False,
        "basicSettings.standaloneSysVmdk": True,
        "basicSettings.lockWindow": False,
        "advancedSettings.micphoneName": "",
        "advancedSettings.speakerName": "",
        "networkSettings.networkEnable": True,
        "networkSettings.networkSwitching": False,
        "networkSettings.networkStatic": False,
        "networkSettings.networkAddress": "0.0.0.0",
        "networkSettings.networkGateway": "0.0.0.0",
        "networkSettings.networkSubnetMask": "255.255.255.0",
        "networkSettings.networkDNS1": "8.8.8.8",
        "networkSettings.networkDNS2": "8.8.4.4",
        "networkSettings.networkInterface": "",
        "basicSettings.disableMouseFastOpt": True,
        "basicSettings.cjztdisableMouseFastOpt_new": 0,
        "basicSettings.HDRQuality": 0,
        "basicSettings.qjcjdisableMouseFast": 1,
        "basicSettings.fps": 60,
        "basicSettings.astc": True,
        "hotkeySettings.backKey": {"modifiers": 0, "key": 27},
        "hotkeySettings.homeKey": {"modifiers": 0, "key": 112},
        "hotkeySettings.appSwitchKey": {"modifiers": 0, "key": 113},
        "hotkeySettings.menuKey": {"modifiers": 0, "key": 114},
        "hotkeySettings.zoomInKey": {"modifiers": 0, "key": 115},
        "hotkeySettings.zoomOutKey": {"modifiers": 0, "key": 116},
        "hotkeySettings.bossKey": {"modifiers": 2, "key": 81},
        "hotkeySettings.shakeKey": {"modifiers": 0, "key": 120},
        "hotkeySettings.operationRecordKey": {"modifiers": 0, "key": 121},
        "hotkeySettings.operationRecordPauseKey": {"modifiers": 0, "key": 0},
        "hotkeySettings.operationRecordShowFrame": {"modifiers": 2, "key": 56},
        "hotkeySettings.fullScreenKey": {"modifiers": 0, "key": 122},
        "hotkeySettings.showMappingKey": {"modifiers": 0, "key": 123},
        "hotkeySettings.videoRecordKey": {"modifiers": 0, "key": 119},
        "hotkeySettings.mappingRecordKey": {"modifiers": 0, "key": 117},
        "hotkeySettings.keyboardModelKey": {"modifiers": 2, "key": 70},
    }
    newfolder = create_independent_instance(
        basic_config=basic_configuration,
        vboxmanage_path=r"C:\Program Files\Oracle\VirtualBox\VBoxManage.exe",
        ldplayer_folder=r"C:\LDPlayer",
    )
    print(newfolder)
