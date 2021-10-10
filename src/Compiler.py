import os

os.system('''\
    pyinstaller --noconfirm --onefile --windowed --icon \
    "F:/PYTHON/TWICH_CHECKER/Twitch_checker_3.2/Presets/icon.ico" \
    --add-data "F:/PYTHON/TWICH_CHECKER/Twitch_checker_3.2/AdvancedToolLayoutPackage;AdvancedToolLayoutPackage/" \
    --add-data "F:/PYTHON/TWICH_CHECKER/Twitch_checker_3.2/ProfileHidenLayoutPackage;ProfileHidenLayoutPackage/" \
    --add-data "F:/PYTHON/TWICH_CHECKER/Twitch_checker_3.2/ProfileLayoutPackage;ProfileLayoutPackage/" \
    --add-data "F:/PYTHON/TWICH_CHECKER/Twitch_checker_3.2/Config.py;." \
    --add-data "F:/PYTHON/TWICH_CHECKER/Twitch_checker_3.2/Constants.py;." \
    --add-data "F:/PYTHON/TWICH_CHECKER/Twitch_checker_3.2/CustomButtonModule.py;." \
    "F:/PYTHON/TWICH_CHECKER/Twitch_checker_3.2/TwitchChecker-v3.2.py"
''')