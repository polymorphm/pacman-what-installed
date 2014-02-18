pacman-what-installed
=====================

``pacman-what-installed`` is tiny tool, that show (in nice view)
what packages are installed on computer.

It is wrapper over tool ``pacman``.

Status
------

Developer version (git master).

Usage Example
-------------

typical usage:

    $ nano ~/Desktop/my_installed_groups
    
    $ cat ~/Desktop/my_installed_groups
    base
    base-devel
    gnome
    gnome-extra
    libreoffice
    
    $ ./pacman-what-installed ~/Desktop/my_installed_groups
    explicit installed:
        alsa-utils
        btrfs-progs
        cups
        cups-filters
        dosfstools
        efibootmgr
        filezilla
        firefox
        foomatic-db
        foomatic-db-engine
        foomatic-db-nonfree
        foomatic-filters
        gimp
        git
        google-talkplugin
        grub
        gst-libav
        gst-plugins-ugly
        gutenprint
        hdparm
        hplip
        hplip-plugin
        imagemagick
        jshon
        libreoffice-en-GB
        miredo
        ntfs-3g
        openssh
        os-prober
        p7zip
        parted
        ppp
        python
        smartmontools
        telepathy-gabble
        telepathy-rakia
        transmission-gtk
        unrar
        wget
        wpa_supplicant
        xf86-input-synaptics
        xf86-video-intel
    
    base group:
        bash
        bzip2
        coreutils
        cronie
        cryptsetup
        device-mapper
        dhcpcd
        diffutils
        e2fsprogs
        file
        filesystem
        findutils
        gawk
        gcc-libs
        gettext
        glibc
        grep
        gzip
        heirloom-mailx
        inetutils
        iproute2
        iputils
        jfsutils
        less
        licenses
        linux
        logrotate
        lvm2
        man-db
        man-pages
        mdadm
        nano
        netctl
        pacman
        pciutils
        pcmciautils
        perl
        procps-ng
        psmisc
        reiserfsprogs
        sed
        shadow
        sysfsutils
        systemd-sysvcompat
        tar
        texinfo
        usbutils
        util-linux
        vi
        which
        xfsprogs
    
    base-devel group:
        autoconf
        automake
        binutils
        bison
        fakeroot
        file
        findutils
        flex
        gawk
        gcc
        gettext
        grep
        groff
        gzip
        libtool
        m4
        make
        pacman
        patch
        pkg-config
        sed
        sudo
        texinfo
        util-linux
        which
    
    gnome group:
        baobab
        empathy
        eog
        epiphany
        evince
        gdm
        gnome-backgrounds
        gnome-calculator
        gnome-contacts
        gnome-control-center
        gnome-desktop
        gnome-dictionary
        gnome-disk-utility
        gnome-font-viewer
        gnome-icon-theme
        gnome-icon-theme-extras
        gnome-icon-theme-symbolic
        gnome-keyring
        gnome-screenshot
        gnome-session
        gnome-settings-daemon
        gnome-shell
        gnome-system-log
        gnome-system-monitor
        gnome-terminal
        gnome-themes-standard
        gnome-user-docs
        gnome-user-share
        mousetweaks
        mutter
        nautilus
        sushi
        totem
        tracker
        vino
        xdg-user-dirs-gtk
        yelp
    
    gnome-extra group:
        accerciser
        aisleriot
        anjuta
        brasero
        cheese
        evolution
        file-roller
        five-or-more
        four-in-a-row
        gedit
        gnome-chess
        gnome-clocks
        gnome-color-manager
        gnome-devel-docs
        gnome-documents
        gnome-getting-started-docs
        gnome-klotski
        gnome-mahjongg
        gnome-mines
        gnome-nettool
        gnome-nibbles
        gnome-photos
        gnome-robots
        gnome-sudoku
        gnome-tetravex
        gnome-weather
        iagno
        lightsoff
        orca
        quadrapassel
        rygel
        seahorse
        swell-foop
        tali
        vinagre
    
    libreoffice group:
        libreoffice-base
        libreoffice-calc
        libreoffice-common
        libreoffice-draw
        libreoffice-gnome
        libreoffice-impress
        libreoffice-math
        libreoffice-writer
        libreoffice-kde4 [not installed for this group]
        libreoffice-postgresql-connector [not installed for this group]
        libreoffice-sdk [not installed for this group]
        libreoffice-sdk-doc [not installed for this group]

But see next:

    $ pacman -Qi xf86-input-synaptics | grep -i groups
    Groups         : xorg-drivers  xorg

Example With Fake Groups
-------------

Next example will show how to using two "fake" groups (``my-cpp-devel`` and ``my-python-devel``)

    $ nano ~/Desktop/my_installed_groups
    
    $ cat ~/Desktop/my_installed_groups
    base
    base-devel
    fake: my-cpp-devel: nano gcc gdc make
    fake: my-python-devel: nano python
    gnome
    gnome-extra
    libreoffice
