from consolectrlchandler import ctrl_config


def ctrlhandler(ctrl_type: str):
    print(f"ctrl handler {ctrl_type}")


ctrl_config.function = ctrlhandler
import os
from list_all_files_recursively_short import (
    get_folder_file_complete_path,
    get_short_path_name,
)
from reggisearch import search_values
import subprocess
import time
from exceptdrucker import errwrite
from killallappsinfolder import ProcKiller
import shutil
import uuid

from flatten_any_dict_iterable_or_whatsoever import (
    fla_tu,
    set_in_original_iter,
    get_from_original_iter,
)
from rootstacks import root_bluestacks

import json
import xmltodict
from typing import Literal, Union

rvc64_basis_modell = r'''bst.instance.Rvc64_NEWID.abi_list="x86,x64,arm,arm64"
bst.instance.Rvc64_NEWID.adb_port="ADBPORTNEW"
bst.instance.Rvc64_NEWID.ads_display_time=""
bst.instance.Rvc64_NEWID.airplane_mode_active="0"
bst.instance.Rvc64_NEWID.airplane_mode_active_time=""
bst.instance.Rvc64_NEWID.android_google_ad_id=""
bst.instance.Rvc64_NEWID.android_id="ANDROID_ID_NEW"
bst.instance.Rvc64_NEWID.android_sound_while_tapping="0"
bst.instance.Rvc64_NEWID.app_launch_count="0"
bst.instance.Rvc64_NEWID.astc_decoding_mode="software"
bst.instance.Rvc64_NEWID.autohide_notifications="0"
bst.instance.Rvc64_NEWID.boot_duration="-1"
bst.instance.Rvc64_NEWID.camera_device=""
bst.instance.Rvc64_NEWID.cpus="4"
bst.instance.Rvc64_NEWID.custom_resolution_selected="0"
bst.instance.Rvc64_NEWID.device_carrier_code="se_72405"
bst.instance.Rvc64_NEWID.device_country_code="076"
bst.instance.Rvc64_NEWID.device_custom_brand=""
bst.instance.Rvc64_NEWID.device_custom_manufacturer=""
bst.instance.Rvc64_NEWID.device_custom_model=""
bst.instance.Rvc64_NEWID.device_profile_code="sttu"
bst.instance.Rvc64_NEWID.display_name="Rvc64_NEWID"
bst.instance.Rvc64_NEWID.dpi="160"
bst.instance.Rvc64_NEWID.eco_mode_max_fps="5"
bst.instance.Rvc64_NEWID.enable_fps_display="0"
bst.instance.Rvc64_NEWID.enable_fullscreen_all_apps="0"
bst.instance.Rvc64_NEWID.enable_high_fps="0"
bst.instance.Rvc64_NEWID.enable_logcat_redirection="0"
bst.instance.Rvc64_NEWID.enable_notifications="0"
bst.instance.Rvc64_NEWID.enable_root_access="0"
bst.instance.Rvc64_NEWID.enable_vsync="0"
bst.instance.Rvc64_NEWID.fb_height="1280"
bst.instance.Rvc64_NEWID.fb_width="720"
bst.instance.Rvc64_NEWID.first_boot="1"
bst.instance.Rvc64_NEWID.game_controls_enabled="0"
bst.instance.Rvc64_NEWID.gl_win_height="-1"
bst.instance.Rvc64_NEWID.gl_win_screen=""
bst.instance.Rvc64_NEWID.gl_win_x="0"
bst.instance.Rvc64_NEWID.gl_win_y="0"
bst.instance.Rvc64_NEWID.google_account_logins=""
bst.instance.Rvc64_NEWID.google_login_popup_shown="0"
bst.instance.Rvc64_NEWID.graphics_engine="aga"
bst.instance.Rvc64_NEWID.graphics_renderer="gl"
bst.instance.Rvc64_NEWID.grm_ignored_rules=""
bst.instance.Rvc64_NEWID.launch_date=""
bst.instance.Rvc64_NEWID.libc_mem_allocator="jem"
bst.instance.Rvc64_NEWID.macro_win_height="-1"
bst.instance.Rvc64_NEWID.macro_win_screen=""
bst.instance.Rvc64_NEWID.macro_win_x="-1"
bst.instance.Rvc64_NEWID.macro_win_y="-1"
bst.instance.Rvc64_NEWID.max_fps="60"
bst.instance.Rvc64_NEWID.pin_to_top="0"
bst.instance.Rvc64_NEWID.ram="4096"
bst.instance.Rvc64_NEWID.show_sidebar="1"
bst.instance.Rvc64_NEWID.status.adb_port="5555"
bst.instance.Rvc64_NEWID.status.ip_addr_prefix_len="24"
bst.instance.Rvc64_NEWID.status.ip_gateway_addr="10.0.2.2"
bst.instance.Rvc64_NEWID.status.ip_guest_addr="10.0.2.15"
bst.instance.Rvc64_NEWID.status.session_id="0"
bst.instance.Rvc64_NEWID.vulkan_supported="1"'''

pie64_basis_modell = r'''
bst.instance.Pie64_NEWID.abi_list="x86,x64,arm,arm64"
bst.instance.Pie64_NEWID.adb_port="ADBPORTNEW"
bst.instance.Pie64_NEWID.ads_display_time=""
bst.instance.Pie64_NEWID.airplane_mode_active="0"
bst.instance.Pie64_NEWID.airplane_mode_active_time=""
bst.instance.Pie64_NEWID.android_google_ad_id=""
bst.instance.Pie64_NEWID.android_id="ANDROID_ID_NEW"
bst.instance.Pie64_NEWID.android_sound_while_tapping="0"
bst.instance.Pie64_NEWID.app_launch_count="0"
bst.instance.Pie64_NEWID.astc_decoding_mode="software"
bst.instance.Pie64_NEWID.autohide_notifications="0"
bst.instance.Pie64_NEWID.boot_duration="-1"
bst.instance.Pie64_NEWID.camera_device=""
bst.instance.Pie64_NEWID.cpus="4"
bst.instance.Pie64_NEWID.custom_resolution_selected="0"
bst.instance.Pie64_NEWID.device_carrier_code="se_72405"
bst.instance.Pie64_NEWID.device_country_code="076"
bst.instance.Pie64_NEWID.device_custom_brand=""
bst.instance.Pie64_NEWID.device_custom_manufacturer=""
bst.instance.Pie64_NEWID.device_custom_model=""
bst.instance.Pie64_NEWID.device_profile_code="sttu"
bst.instance.Pie64_NEWID.display_name="Pie64_NEWID"
bst.instance.Pie64_NEWID.dpi="240"
bst.instance.Pie64_NEWID.eco_mode_max_fps="5"
bst.instance.Pie64_NEWID.enable_fps_display="0"
bst.instance.Pie64_NEWID.enable_fullscreen_all_apps="0"
bst.instance.Pie64_NEWID.enable_high_fps="0"
bst.instance.Pie64_NEWID.enable_logcat_redirection="0"
bst.instance.Pie64_NEWID.enable_notifications="0"
bst.instance.Pie64_NEWID.enable_root_access="0"
bst.instance.Pie64_NEWID.enable_vsync="0"
bst.instance.Pie64_NEWID.fb_height="1280"
bst.instance.Pie64_NEWID.fb_width="720"
bst.instance.Pie64_NEWID.first_boot="1"
bst.instance.Pie64_NEWID.game_controls_enabled="0"
bst.instance.Pie64_NEWID.gl_win_height="-1"
bst.instance.Pie64_NEWID.gl_win_screen=""
bst.instance.Pie64_NEWID.gl_win_x="0"
bst.instance.Pie64_NEWID.gl_win_y="0"
bst.instance.Pie64_NEWID.google_account_logins=""
bst.instance.Pie64_NEWID.google_login_popup_shown="0"
bst.instance.Pie64_NEWID.graphics_engine="aga"
bst.instance.Pie64_NEWID.graphics_renderer="gl"
bst.instance.Pie64_NEWID.grm_ignored_rules=""
bst.instance.Pie64_NEWID.launch_date=""
bst.instance.Pie64_NEWID.libc_mem_allocator="jem"
bst.instance.Pie64_NEWID.macro_win_height="-1"
bst.instance.Pie64_NEWID.macro_win_screen=""
bst.instance.Pie64_NEWID.macro_win_x="-1"
bst.instance.Pie64_NEWID.macro_win_y="-1"
bst.instance.Pie64_NEWID.max_fps="60"
bst.instance.Pie64_NEWID.pin_to_top="0"
bst.instance.Pie64_NEWID.ram="4096"
bst.instance.Pie64_NEWID.show_sidebar="0"
bst.instance.Pie64_NEWID.status.adb_port="5555"
bst.instance.Pie64_NEWID.status.ip_addr_prefix_len="24"
bst.instance.Pie64_NEWID.status.ip_gateway_addr="10.0.2.2"
bst.instance.Pie64_NEWID.status.ip_guest_addr="10.0.2.15"
bst.instance.Pie64_NEWID.status.session_id="0"
bst.instance.Pie64_NEWID.vulkan_supported="1"'''


nougat64_basis_modell = r"""
bst.instance.Nougat64_NEWID.adb_port="ADBPORTNEW"
bst.instance.Nougat64_NEWID.ads_display_time=""
bst.instance.Nougat64_NEWID.airplane_mode_active="0"
bst.instance.Nougat64_NEWID.airplane_mode_active_time=""
bst.instance.Nougat64_NEWID.android_google_ad_id=""
bst.instance.Nougat64_NEWID.android_id="ANDROID_ID_NEW"
bst.instance.Nougat64_NEWID.android_sound_while_tapping="0"
bst.instance.Nougat64_NEWID.app_launch_count="0"
bst.instance.Nougat64_NEWID.astc_decoding_mode="software"
bst.instance.Nougat64_NEWID.autohide_notifications="0"
bst.instance.Nougat64_NEWID.boot_duration="-1"
bst.instance.Nougat64_NEWID.camera_device=""
bst.instance.Nougat64_NEWID.cpus="4"
bst.instance.Nougat64_NEWID.custom_resolution_selected="0"
bst.instance.Nougat64_NEWID.device_carrier_code="se_72405"
bst.instance.Nougat64_NEWID.device_country_code="076"
bst.instance.Nougat64_NEWID.device_custom_brand=""
bst.instance.Nougat64_NEWID.device_custom_manufacturer=""
bst.instance.Nougat64_NEWID.device_custom_model=""
bst.instance.Nougat64_NEWID.device_profile_code="stul"
bst.instance.Nougat64_NEWID.display_name="Nougat64_NEWID"
bst.instance.Nougat64_NEWID.dpi="240"
bst.instance.Nougat64_NEWID.eco_mode_max_fps="5"
bst.instance.Nougat64_NEWID.enable_fps_display="0"
bst.instance.Nougat64_NEWID.enable_fullscreen_all_apps="0"
bst.instance.Nougat64_NEWID.enable_high_fps="0"
bst.instance.Nougat64_NEWID.enable_logcat_redirection="0"
bst.instance.Nougat64_NEWID.enable_notifications="0"
bst.instance.Nougat64_NEWID.enable_root_access="0"
bst.instance.Nougat64_NEWID.enable_vsync="0"
bst.instance.Nougat64_NEWID.fb_height="1280"
bst.instance.Nougat64_NEWID.fb_width="720"
bst.instance.Nougat64_NEWID.first_boot="1"
bst.instance.Nougat64_NEWID.game_controls_enabled="0"
bst.instance.Nougat64_NEWID.gl_win_height="-1"
bst.instance.Nougat64_NEWID.gl_win_screen=""
bst.instance.Nougat64_NEWID.gl_win_x="0"
bst.instance.Nougat64_NEWID.gl_win_y="0"
bst.instance.Nougat64_NEWID.google_account_logins=""
bst.instance.Nougat64_NEWID.google_login_popup_shown="0"
bst.instance.Nougat64_NEWID.graphics_engine="aga"
bst.instance.Nougat64_NEWID.graphics_renderer="gl"
bst.instance.Nougat64_NEWID.grm_ignored_rules=""
bst.instance.Nougat64_NEWID.launch_date=""
bst.instance.Nougat64_NEWID.libc_mem_allocator="jem"
bst.instance.Nougat64_NEWID.macro_win_height="-1"
bst.instance.Nougat64_NEWID.macro_win_screen=""
bst.instance.Nougat64_NEWID.macro_win_x="-1"
bst.instance.Nougat64_NEWID.macro_win_y="-1"
bst.instance.Nougat64_NEWID.max_fps="60"
bst.instance.Nougat64_NEWID.pin_to_top="0"
bst.instance.Nougat64_NEWID.ram="4096"
bst.instance.Nougat64_NEWID.show_sidebar="1"
bst.instance.Nougat64_NEWID.status.adb_port="5555"
bst.instance.Nougat64_NEWID.status.ip_addr_prefix_len="24"
bst.instance.Nougat64_NEWID.status.ip_gateway_addr="10.0.2.2"
bst.instance.Nougat64_NEWID.status.ip_guest_addr="10.0.2.15"
bst.instance.Nougat64_NEWID.status.session_id="0"
bst.instance.Nougat64_NEWID.vulkan_supported="1"
"""
nougat32_basis_modell = r'''
bst.instance.Nougat32_NEWID.abi_list="x86,arm"
bst.instance.Nougat32_NEWID.adb_port="ADBPORTNEW"
bst.instance.Nougat32_NEWID.ads_display_time=""
bst.instance.Nougat32_NEWID.airplane_mode_active="0"
bst.instance.Nougat32_NEWID.airplane_mode_active_time=""
bst.instance.Nougat32_NEWID.android_google_ad_id=""
bst.instance.Nougat32_NEWID.android_id="ANDROID_ID_NEW"
bst.instance.Nougat32_NEWID.android_sound_while_tapping="0"
bst.instance.Nougat32_NEWID.app_launch_count="0"
bst.instance.Nougat32_NEWID.astc_decoding_mode="software"
bst.instance.Nougat32_NEWID.autohide_notifications="0"
bst.instance.Nougat32_NEWID.boot_duration="-1"
bst.instance.Nougat32_NEWID.camera_device=""
bst.instance.Nougat32_NEWID.cpus="4"
bst.instance.Nougat32_NEWID.custom_resolution_selected="0"
bst.instance.Nougat32_NEWID.device_carrier_code="se_72405"
bst.instance.Nougat32_NEWID.device_country_code="076"
bst.instance.Nougat32_NEWID.device_custom_brand=""
bst.instance.Nougat32_NEWID.device_custom_manufacturer=""
bst.instance.Nougat32_NEWID.device_custom_model=""
bst.instance.Nougat32_NEWID.device_profile_code="ofpn"
bst.instance.Nougat32_NEWID.display_name="Nougat32_NEWID"
bst.instance.Nougat32_NEWID.dpi="240"
bst.instance.Nougat32_NEWID.eco_mode_max_fps="5"
bst.instance.Nougat32_NEWID.enable_fps_display="0"
bst.instance.Nougat32_NEWID.enable_fullscreen_all_apps="0"
bst.instance.Nougat32_NEWID.enable_high_fps="0"
bst.instance.Nougat32_NEWID.enable_logcat_redirection="0"
bst.instance.Nougat32_NEWID.enable_notifications="0"
bst.instance.Nougat32_NEWID.enable_root_access="0"
bst.instance.Nougat32_NEWID.enable_vsync="0"
bst.instance.Nougat32_NEWID.fb_height="1280"
bst.instance.Nougat32_NEWID.fb_width="720"
bst.instance.Nougat32_NEWID.first_boot="1"
bst.instance.Nougat32_NEWID.game_controls_enabled="0"
bst.instance.Nougat32_NEWID.gl_win_height="-1"
bst.instance.Nougat32_NEWID.gl_win_screen=""
bst.instance.Nougat32_NEWID.gl_win_x="0"
bst.instance.Nougat32_NEWID.gl_win_y="0"
bst.instance.Nougat32_NEWID.google_account_logins=""
bst.instance.Nougat32_NEWID.google_login_popup_shown="0"
bst.instance.Nougat32_NEWID.graphics_engine="aga"
bst.instance.Nougat32_NEWID.graphics_renderer="gl"
bst.instance.Nougat32_NEWID.grm_ignored_rules=""
bst.instance.Nougat32_NEWID.launch_date=""
bst.instance.Nougat32_NEWID.libc_mem_allocator="jem"
bst.instance.Nougat32_NEWID.macro_win_height="-1"
bst.instance.Nougat32_NEWID.macro_win_screen=""
bst.instance.Nougat32_NEWID.macro_win_x="-1"
bst.instance.Nougat32_NEWID.macro_win_y="-1"
bst.instance.Nougat32_NEWID.max_fps="60"
bst.instance.Nougat32_NEWID.pin_to_top="0"
bst.instance.Nougat32_NEWID.ram="4096"
bst.instance.Nougat32_NEWID.show_sidebar="1"
bst.instance.Nougat32_NEWID.status.adb_port="5555"
bst.instance.Nougat32_NEWID.status.ip_addr_prefix_len="24"
bst.instance.Nougat32_NEWID.status.ip_gateway_addr="10.0.2.2"
bst.instance.Nougat32_NEWID.status.ip_guest_addr="10.0.2.15"
bst.instance.Nougat32_NEWID.status.session_id="0"
bst.instance.Nougat32_NEWID.vulkan_supported="1"'''

startupinfo = subprocess.STARTUPINFO()
startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
startupinfo.wShowWindow = subprocess.SW_HIDE
creationflags = subprocess.CREATE_NO_WINDOW
invisibledict = {
    "startupinfo": startupinfo,
    "creationflags": creationflags,
    "start_new_session": True,
}


def create_android_id():
    return "".join(str(uuid.uuid1()).split("-")[-2:])


def get_timest():
    return time.strftime("%Y_%m_%d_%H_%M_%S")


def parse_bluestacks_conf(bstconfigpath):
    with open(bstconfigpath, mode="r", encoding="utf-8") as f:
        data = f.read()

    maxinstance = 1
    instancedata = {}
    for d in data.splitlines():
        dsplit = d.split(".")
        try:
            if dsplit[0] == "bst" and dsplit[1] == "instance":
                if dsplit[2] not in instancedata:
                    instancedata[dsplit[2]] = {}
                try:
                    splitdata = d.rsplit("=", maxsplit=1)

                    instancedata[dsplit[2]][
                        splitdata[0].rsplit(".", maxsplit=1)[-1]
                    ] = splitdata[-1]
                except Exception:
                    pass
                numbernow = int(dsplit[2].split("_")[-1])
                if numbernow > maxinstance:
                    maxinstance = numbernow

        except Exception:
            pass
    return instancedata, maxinstance


def get_bluestacks_programm_data_folder():
    di = search_values(
        mainkeys=r"HKEY_LOCAL_MACHINE\SOFTWARE\BlueStacks_nxt", subkeys="UserDefinedDir"
    )
    bstconfigpath_folder = di[r"HKEY_LOCAL_MACHINE\SOFTWARE\BlueStacks_nxt"][
        "UserDefinedDir"
    ]
    bstconfigpath = os.path.normpath(
        os.path.join(bstconfigpath_folder, "bluestacks.conf")
    )

    di2 = search_values(
        mainkeys=r"HKEY_LOCAL_MACHINE\SOFTWARE\BlueStacks_nxt", subkeys="InstallDir"
    )
    bstexe_folder = di2[r"HKEY_LOCAL_MACHINE\SOFTWARE\BlueStacks_nxt"]["InstallDir"]
    bsthdplayer = os.path.normpath(os.path.join(bstexe_folder, "HD-Player.exe"))

    vboxmanager = os.path.normpath(os.path.join(bstexe_folder, "BstkVMMgr.exe"))

    return (
        bstconfigpath_folder,
        bstconfigpath,
        get_short_path_name(bstconfigpath_folder),
        get_short_path_name(bstconfigpath),
        bstexe_folder,
        bsthdplayer,
        get_short_path_name(bstexe_folder),
        get_short_path_name(bsthdplayer),
        vboxmanager,
        get_short_path_name(vboxmanager),
    )


def create_bluestacks_instance(
    base_instance_to_create="Pie64",
    newtype_fastboot="Normal",
    newtype_root="Normal",
    newtype_data="Normal",
):
    allbstacksfiles = get_folder_file_complete_path(bstconfigpath_folder)
    original_bstacks_files = [
        x for x in allbstacksfiles if x.file.lower() == "data_orig.vhdx"
    ]
    all_files_original_bstacks_files = {}
    all_files_original_instance_numbers = {}
    all_important_basic_files = {}
    for f in allbstacksfiles:
        for of in original_bstacks_files:
            if f.folder == of.folder:
                all_files_original_bstacks_files.setdefault(
                    f.folder.split(os.sep)[-1], []
                ).append(f)
        if f.file.lower() == "data.vhdx":
            newkey = f.folder.split(os.sep)[-1]
            try:
                keytoadd, newvalue = newkey.strip().split("_")
                newvalue = int(newvalue)
                all_files_original_instance_numbers.setdefault(keytoadd, []).append(
                    newvalue
                )

            except Exception:
                pass
    highest_instances = {
        k: max(v) for k, v in all_files_original_instance_numbers.items() if v[0]
    }
    for k, v in all_files_original_bstacks_files.items():
        if k not in all_important_basic_files:
            all_important_basic_files[k] = {}
            try:
                all_important_basic_files[k]["last_instance"] = highest_instances[k]
            except Exception:
                all_important_basic_files[k]["last_instance"] = 0
        for bstackfile in v:
            lowerfile = bstackfile.file.lower()
            if lowerfile == (k + ".bstk").lower():
                all_important_basic_files[k]["bstk"] = bstackfile
            elif lowerfile == "fastboot.vdi":
                all_important_basic_files[k]["fastboot"] = bstackfile
            elif lowerfile == "data_orig.vhdx":
                all_important_basic_files[k]["data"] = bstackfile
            elif lowerfile == "root.vhd":
                all_important_basic_files[k]["root"] = bstackfile

    index_for_instance = maxinstance + 1

    newfolder = (
        all_important_basic_files[base_instance_to_create]["data"].folder
        + "_"
        + str(index_for_instance)
    )
    os.makedirs(newfolder, exist_ok=True)
    pure_instance_name = newfolder.split(os.sep)[-1]
    newdatavhdx = os.path.join(newfolder, "Data.vhdx")
    newbstk = os.path.join(newfolder, pure_instance_name + ".bstk")
    newfastboot = os.path.join(newfolder, "fastboot.vdi")
    newroot = os.path.join(newfolder, "Root.vhd")

    shutil.copyfile(
        all_important_basic_files[base_instance_to_create]["data"].path, newdatavhdx
    )
    shutil.copyfile(
        all_important_basic_files[base_instance_to_create]["bstk"].path, newbstk
    )
    shutil.copyfile(
        all_important_basic_files[base_instance_to_create]["fastboot"].path, newfastboot
    )
    shutil.copyfile(
        all_important_basic_files[base_instance_to_create]["root"].path, newroot
    )

    uuid_datavhdx = str(uuid.uuid4())
    uuid_rootvhd = str(uuid.uuid4())

    uuid_fastbootvdi = str(uuid.uuid4())

    uuidchangecmd1 = rf"""{vboxmanager_short} internalcommands sethduuid {newdatavhdx} {uuid_datavhdx}"""
    subprocess.run(uuidchangecmd1, shell=True, capture_output=False, **invisibledict)

    uuidchangecmd2 = (
        rf"""{vboxmanager_short} internalcommands sethduuid {newroot} {uuid_rootvhd}"""
    )
    subprocess.run(uuidchangecmd2, shell=True, capture_output=False, **invisibledict)

    uuidchangecmd3 = rf"""{vboxmanager_short} internalcommands sethduuid {newfastboot} {uuid_fastbootvdi}"""
    subprocess.run(uuidchangecmd3, shell=True, capture_output=False, **invisibledict)

    with open(newbstk, "r", encoding="utf-8") as f:
        bstackscontent = f.read()

    bstacksdict = xmltodict.parse(bstackscontent)
    pki.kill_running_procs()
    changeddata = {}

    lookupdict = {}
    uuid_fastbootvdi = f"{{{uuid_fastbootvdi}}}"
    uuid_rootvhd = f"{{{uuid_rootvhd}}}"
    uuid_datavhdx = f"{{{uuid_datavhdx}}}"
    for v, k in tuple(fla_tu(bstacksdict)):
        try:
            if k[-1] == "@uuid" and isinstance(k[-2], int) and k[-3] == "HardDisk":
                print(k, v)
                klocation = k[:-1] + ("@location",)
                ktype = k[:-1] + ("@type",)
                newkey = get_from_original_iter(bstacksdict, klocation)
                changeddata[newkey] = {
                    "old_@type": get_from_original_iter(bstacksdict, ktype),
                    "old_@uuid": v,
                }
                if newkey.lower() == "fastboot.vdi":
                    set_in_original_iter(bstacksdict, k, uuid_fastbootvdi)
                    set_in_original_iter(bstacksdict, ktype, newtype_fastboot)
                    changeddata[newkey]["new_@type"] = newtype_fastboot
                    changeddata[newkey]["new_@uuid"] = uuid_fastbootvdi
                elif newkey.lower() == "root.vhd":
                    set_in_original_iter(bstacksdict, k, uuid_rootvhd)
                    set_in_original_iter(bstacksdict, ktype, newtype_root)
                    changeddata[newkey]["new_@type"] = newtype_root
                    changeddata[newkey]["new_@uuid"] = uuid_rootvhd
                elif newkey.lower() == "data.vhdx":
                    set_in_original_iter(bstacksdict, k, uuid_datavhdx)
                    set_in_original_iter(bstacksdict, ktype, newtype_data)
                    changeddata[newkey]["new_@type"] = newtype_data
                    changeddata[newkey]["new_@uuid"] = uuid_datavhdx
                lookupdict[changeddata[newkey]["old_@uuid"]] = changeddata[newkey][
                    "new_@uuid"
                ]
        except Exception:
            errwrite()

    for v, k in tuple(fla_tu(bstacksdict)):
        if v in lookupdict:
            set_in_original_iter(bstacksdict, k, lookupdict[v])
    newmachineuuid = str(uuid.uuid4())
    set_in_original_iter(
        bstacksdict, ("VirtualBox", "Machine", "@uuid"), "{" + newmachineuuid + "}"
    )
    set_in_original_iter(
        bstacksdict, ("VirtualBox", "Machine", "@name"), pure_instance_name
    )

    sharedfolderpath = os.path.join(
        bstconfigpath_folder, "Engine", "UserData", "SharedFolder"
    )
    os.makedirs(sharedfolderpath, exist_ok=True)
    for v, k in fla_tu(bstacksdict):
        try:
            if (
                k[-1] == "@hostPath"
                and isinstance(k[-2], int)
                and k[-3] == "SharedFolder"
            ):
                if "InputMapper" not in v:
                    set_in_original_iter(bstacksdict, k, sharedfolderpath)
        except Exception:
            errwrite()

    xml_to_save = xmltodict.unparse(bstacksdict)

    with open(newbstk, "w", encoding="utf-8") as f:
        f.write(xml_to_save)

    subprocess.run(
        rf"""{vboxmanager_short} registervm {newbstk}""",
        shell=False,
        **invisibledict,
    )
    return pure_instance_name, bstacksdict


def update_bstacks_config_files(configfile, allpreconfigfiles):
    tstamp = get_timest()

    configfilebackup = configfile.replace(".conf", f"_{tstamp}.conf")
    jsonmenufile = os.path.join(
        bstconfigpath_folder, "Engine", "UserData", "MimMetaData.json"
    )

    alladbports = set()
    with open(configfile, mode="r", encoding="utf-8") as f:
        data = f.read()
    with open(configfilebackup, mode="w", encoding="utf-8") as f:
        f.write(data)
    for d in data.splitlines():
        try:
            alladbports.add(int(d.split('adb_port="')[1].strip('"')))
        except Exception:
            pass

    adbportnextonefree = 5560
    while adbportnextonefree in alladbports:
        adbportnextonefree += 5
    basisinstance = instancename.split("_")[0]
    splitline = "bst.instance." + basisinstance + "_"
    top, bottom = data.rsplit(splitline, maxsplit=1)
    bottomsplitlines = bottom.splitlines()
    bottom = "\n".join(bottomsplitlines[1:])
    top = top + splitline + bottomsplitlines[0]
    newandroidid = create_android_id()
    configupdated = (
        allpreconfigfiles[basisinstance]
        .replace(basisinstance + "_NEWID", instancename)
        .replace(
            "ADBPORTNEW",
            str(adbportnextonefree),
        )
        # .replace(f"{basisinstance}_NEWID", "")
        .replace("ANDROID_ID_NEW", newandroidid)
    )
    newfiledata = top.strip() + "\n" + configupdated.strip() + "\n" + bottom.strip()

    with open(configfile, mode="w", encoding="utf-8") as f:
        f.write(newfiledata)

    with open(jsonmenufile, mode="r", encoding="utf-8") as f:
        jsondata = f.read()
    datadict = json.loads(jsondata)
    highestid = 0
    fistkey = ""
    for v, k in fla_tu(datadict):
        fistkey = k[0]
        if k[-1] == "ID":
            if int(v) > highestid:
                highestid = int(v)

    datadict[fistkey].append(
        {
            "ID": highestid + 1,
            "Name": instancename,
            "IsFolder": False,
            "ParentFolder": -1,
            "IsOpen": False,
            "IsVisible": True,
            "InstanceName": instancename,
        }
    )
    updatedjson = json.dumps(datadict, indent=4)
    with open(jsonmenufile, mode="w", encoding="utf-8") as f:
        f.write(updatedjson)
    return adbportnextonefree


(
    bstconfigpath_folder,
    bstconfigpath,
    bstconfigpath_folder_short,
    bstconfigpath_short,
    bstexe_folder,
    bsthdplayer,
    bstexe_folder_short,
    bsthdplayer_short,
    vboxmanager,
    vboxmanager_short,
) = get_bluestacks_programm_data_folder()
bluestacksconf_instances, maxinstance = parse_bluestacks_conf(bstconfigpath_short)
instancename = ""
pki = ProcKiller(
    folders=(
        bstexe_folder,
        bstexe_folder_short,
        bstconfigpath_folder_short,
        bstconfigpath_folder,
    ),
    kill_timeout=2,
    protect_myself=True,  # important, protect_myselfis False, you might kill the whole python process you are in.
    winkill_sigint_dll=True,  # dll first
    winkill_sigbreak_dll=True,
    winkill_sigint=True,  # exe from outside
    winkill_sigbreak=True,
    powershell_sigint=False,
    powershell_sigbreak=False,
    powershell_close=False,
    multi_children_kill=False,  # try to kill each child one by one
    multi_children_always_ignore_pids=(0, 4),  # ignore system processes
    print_output=True,
    taskkill_as_last_option=True,  # this always works, but it is not gracefully anymore):
    exeendings=(".com", ".exe"),
    filter_function=lambda files: True,
).get_active_procs()
time.sleep(1)


def batch_create_bstacks_instances(
    newintancenametocreate_config: Union[str, None] = None,
    newintancenametocreate: Literal["Rvc64", "Pie64", "Nougat64", "Nougat32"] = "Rvc64",
    newtype_fastboot: Literal["Normal", "ReadOnly"] = "Normal",
    newtype_root: Literal["Normal", "ReadOnly"] = "Normal",
    newtype_data: Literal["Normal", "ReadOnly"] = "Normal",
    numberofinstances=1,
) -> list:
    r"""
            Creates multiple instances of BlueStacks with independent system disk.

            Args:
                newintancenametocreate_config (Union[str, None], optional): The configuration file for the new instance. If provided, it will override the default configuration (pie64_basis_modell, rvc64_basis_modell, nougat64_basis_modell, nougat32_basis_modell). Defaults to None.
                newintancenametocreate (Literal["Rvc64", "Pie64", "Nougat64", "Nougat32"], optional): The name of the new instance. Defaults to "Rvc64".
                newtype_fastboot (Literal["Normal", "ReadOnly"], optional): The type of fastboot for the new instance. Defaults to "Normal".
                newtype_root (Literal["Normal", "ReadOnly"], optional): The type of root for the new instance. Defaults to "Normal".
                newtype_data (Literal["Normal", "ReadOnly"], optional): The type of data for the new instance. Defaults to "Normal".
                numberofinstances (int, optional): The number of instances to create. Defaults to 1.

            Returns:
                list: A list of lists containing the instance name and the adb port for each created instance.
            Example:
                from bluestacks5newinstances import batch_create_bstacks_instances

                # don't change the uppercase letters, they are going to be replaced by the script
                newinstances_and_adbports = batch_create_bstacks_instances(
                    newintancenametocreate_config=r'''bst.instance.Rvc64_NEWID.abi_list="x86,x64,arm,arm64"
                bst.instance.Rvc64_NEWID.adb_port="ADBPORTNEW"
                bst.instance.Rvc64_NEWID.ads_display_time=""
                bst.instance.Rvc64_NEWID.airplane_mode_active="0"
                bst.instance.Rvc64_NEWID.airplane_mode_active_time=""
                bst.instance.Rvc64_NEWID.android_google_ad_id=""
                bst.instance.Rvc64_NEWID.android_id="ANDROID_ID_NEW"
                bst.instance.Rvc64_NEWID.android_sound_while_tapping="0"
                bst.instance.Rvc64_NEWID.app_launch_count="0"
                bst.instance.Rvc64_NEWID.astc_decoding_mode="software"
                bst.instance.Rvc64_NEWID.autohide_notifications="0"
                bst.instance.Rvc64_NEWID.boot_duration="-1"
                bst.instance.Rvc64_NEWID.camera_device=""
                bst.instance.Rvc64_NEWID.cpus="4"
                bst.instance.Rvc64_NEWID.custom_resolution_selected="0"
                bst.instance.Rvc64_NEWID.device_carrier_code="se_72405"
                bst.instance.Rvc64_NEWID.device_country_code="076"
                bst.instance.Rvc64_NEWID.device_custom_brand=""
                bst.instance.Rvc64_NEWID.device_custom_manufacturer=""
                bst.instance.Rvc64_NEWID.device_custom_model=""
                bst.instance.Rvc64_NEWID.device_profile_code="sttu"
                bst.instance.Rvc64_NEWID.display_name="Rvc64_NEWID"
                bst.instance.Rvc64_NEWID.dpi="160"
                bst.instance.Rvc64_NEWID.eco_mode_max_fps="5"
                bst.instance.Rvc64_NEWID.enable_fps_display="0"
                bst.instance.Rvc64_NEWID.enable_fullscreen_all_apps="0"
                bst.instance.Rvc64_NEWID.enable_high_fps="0"
                bst.instance.Rvc64_NEWID.enable_logcat_redirection="0"
                bst.instance.Rvc64_NEWID.enable_notifications="0"
                bst.instance.Rvc64_NEWID.enable_root_access="0"
                bst.instance.Rvc64_NEWID.enable_vsync="0"
                bst.instance.Rvc64_NEWID.fb_height="1280"
                bst.instance.Rvc64_NEWID.fb_width="720"
                bst.instance.Rvc64_NEWID.first_boot="1"
                bst.instance.Rvc64_NEWID.game_controls_enabled="0"
                bst.instance.Rvc64_NEWID.gl_win_height="-1"
                bst.instance.Rvc64_NEWID.gl_win_screen=""
                bst.instance.Rvc64_NEWID.gl_win_x="0"
                bst.instance.Rvc64_NEWID.gl_win_y="0"
                bst.instance.Rvc64_NEWID.google_account_logins=""
                bst.instance.Rvc64_NEWID.google_login_popup_shown="0"
                bst.instance.Rvc64_NEWID.graphics_engine="aga"
                bst.instance.Rvc64_NEWID.graphics_renderer="gl"
                bst.instance.Rvc64_NEWID.grm_ignored_rules=""
                bst.instance.Rvc64_NEWID.launch_date=""
                bst.instance.Rvc64_NEWID.libc_mem_allocator="jem"
                bst.instance.Rvc64_NEWID.macro_win_height="-1"
                bst.instance.Rvc64_NEWID.macro_win_screen=""
                bst.instance.Rvc64_NEWID.macro_win_x="-1"
                bst.instance.Rvc64_NEWID.macro_win_y="-1"
                bst.instance.Rvc64_NEWID.max_fps="60"
                bst.instance.Rvc64_NEWID.pin_to_top="0"
                bst.instance.Rvc64_NEWID.ram="4096"
                bst.instance.Rvc64_NEWID.show_sidebar="1"
                bst.instance.Rvc64_NEWID.status.adb_port="5555"
                bst.instance.Rvc64_NEWID.status.ip_addr_prefix_len="24"
                bst.instance.Rvc64_NEWID.status.ip_gateway_addr="10.0.2.2"
                bst.instance.Rvc64_NEWID.status.ip_guest_addr="10.0.2.15"
                bst.instance.Rvc64_NEWID.status.session_id="0"
                bst.instance.Rvc64_NEWID.vulkan_supported="1"''',
                    newintancenametocreate="Rvc64",
                    newtype_fastboot="Normal",
                    newtype_root="Normal",
                    newtype_data="Normal",
                    numberofinstances=3,
                )
                print(newinstances_and_adbports)
    """
    global instancename, bluestacksconf_instances, maxinstance
    newinstanceslist = []
    pki.kill_running_procs()
    # if len(sys.argv) > 1:
    counterins = 0
    time.sleep(2)
    allpreconfigfiles = {
        "Pie64": pie64_basis_modell,
        "Rvc64": rvc64_basis_modell,
        "Nougat64": nougat64_basis_modell,
        "Nougat32": nougat32_basis_modell,
    }
    if newintancenametocreate_config:
        allpreconfigfiles[newintancenametocreate] = newintancenametocreate_config
    while counterins < numberofinstances:
        try:
            instancename, bstacksdict = create_bluestacks_instance(
                base_instance_to_create=newintancenametocreate,
                newtype_fastboot=newtype_fastboot,
                newtype_root=newtype_root,
                newtype_data=newtype_data,
            )
            time.sleep(3)
            try:
                subprocess.run("taskkill /IM BstkSVC.exe /F", **invisibledict)
            except Exception:
                pass

            adbport = update_bstacks_config_files(
                configfile=bstconfigpath,
                allpreconfigfiles=allpreconfigfiles,
            )
            root_bluestacks(make_read_only=False)  # if make_read_onl
            time.sleep(1)
            bluestacksconf_instances, maxinstance = parse_bluestacks_conf(
                bstconfigpath_short
            )
            newinstanceslist.append([instancename, adbport])
        except Exception:
            errwrite()
        counterins += 1

    return newinstanceslist

