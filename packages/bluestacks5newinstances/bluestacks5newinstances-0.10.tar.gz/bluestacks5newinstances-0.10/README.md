# Creates multiple instances of BlueStacks 5 with an independent system disk.

### Tested against Windows 10 / Python 3.11 / Anaconda

### pip install bluestacks5newinstances


```python
# Install BlueStacks 5
# Create the main emulator and at least one instance of it and run all created instances 


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
```