# m1-multimc-hack

Want to get Minecraft running natively on a Mac with an M1 "Apple Silicon" chip? Thanks to [the excellent work](https://gist.github.com/tanmayb123/d55b16c493326945385e815453de411a) by [Tanmay Bakshi](https://gist.github.com/tanmayb123), it's possible!

This repo contains a wrapper script to be used with [MultiMC](https://multimc.org) that will configure any MultiMC instance to use the Apple Silicon native libraries from Tanmay's work. All you have to do is set the wrapper command and make sure you're using an M1-compatible JDK, and it should just work.

## Setup and Usage

### Pre-requisites

First, install the [Zulu Java 11 JDK for macOS ARM64](https://cdn.azul.com/zulu/bin/zulu11.43.1015-ca-jdk11.0.9.1-macos_aarch64.dmg).

You'll also need a standard install of MultiMC.

### Clone or Download this repo

If you're comfortable with a terminal, open one up and clone this repo somewhere. For examples, let's keep it in `~/stuff`:

```shell
cd ~/stuff
git clone https://github.com/yusefnapora/m1-multimc-hack.git
```

Alternatively, you can download the repository as a zip archive and extract it somewhere.

### Configure MultiMC

Create a new Minecraft instance in MultiMC (or duplicate an existing one), then click "Edit Instance" in the sidebar.

Go to Settings, then make sure the "Java Installation" checkbox is checked. Then hit "Auto-detect", and it should open a window
with a list of Java versions. Find the one that says "zulu-11" and select it, then hit OK.

Still in the Settings pane, switch to the "Custom Commands" tab. Check the "Custom Commands" checkbox. In the "Wrapper Command" box, enter the full path to the `mcwrap.py` script from this repo, e.g. `/Users/your-username/stuff/m1-multimc-hack/mcwrap.py`.

That's it! You should be able to launch the instance and run with native performance.

### Optional - Mods

So far, I haven't had any luck running Forge - I keep hitting LWJGL bugs that crash on launch.

However, Fabric seems to work great, so that's pretty cool :) To install fabric, go to the Version pane of the "Edit Instance" screen, then just hit "Install Fabric". You can then add Fabric mods from the "Loader Mods" pane.