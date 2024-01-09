# Dal Segno Al Kodi

Scan a barcode and play music.

Convert a barcode as scanned from compact disc (e.g. `082839056427`) to a Discogs release (e.g. `41078`), smurf it to a valid pattern such as an artist, year and title (e.g. `DNA ft. SUZANNE VEGA (1990) Tom's Diner`) to locate this on a locally attached network storage (e.g. `\\nas\music\singles\DNA ft. SUZANNE VEGA (1990) Tom's Diner`), and post that request to the API on a Kodi device.

1. Connect a [WS-14810](http://www.waveshare.com/wiki/Barcode_Scanner_Module) barcode scanner to a Raspberry Pi running a Bash shell.  
Append function (`scan_barcode () { ... }`) with a custom [while ... ; do](https://unix.stackexchange.com/a/555628)-loop to the [~/.bashrc](https://superuser.com/a/49292)-file, and call it with ``'curl'`` at the end of the [run command](https://superuser.com/a/144377):

    ```bash
    # .bashrc
    scan_barcode () {
    while read -ra barcode; do
        "$@" "host-running-dal-segno-al-kodi:5000/scan/${barcode[@]}"
    done
    }
    scan_barcode 'curl'
    ```

2. Generate a [Discogs](https://www.discogs.com/settings/developers) personal access token (PAT).  
   Write this token at the `discogs.authorization.personal-access-token`-property in the `dal-segno-al-kodi.config.json` file.
3. Enable Kodi's [JSON RPC API](https://kodi.wiki/view/JSON-RPC_API).  
   Set the [Settings/Services/Control/Allow remote control via HTTP](https://kodi.wiki/view/Settings/Services/Control#Allow_remote_control_via_HTTP)-switch, and specify an username and password.  
   Write the username at the `kodi.authorization.username`-property in the `dal-segno-al-kodi.config.json`-file, and the unencrypted password at `kodi.authorization.password`.  
   In addition, change the `kodi.jsonrpc-uri`-property in the config file to your Kodi server's address.
4. Run with `flask.exe --app '.\dal-segno-al-kodi.py' run --reload --host 0.0.0.0`
5. Scan a barcode, and listen!
