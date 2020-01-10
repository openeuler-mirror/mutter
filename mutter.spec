%global gtk3_ver        3.19.8
%global glib_ver        2.53.2
%global libinput_ver    1.4
%global mutter_api_ver  5
%global pipewire_ver    0.2.2
%global json_glib_ver   0.12.0
%global gsettings_desktop_schemas_ver 3.33.0

%bcond_with profiler

Name:          mutter
Version:       3.34.3
Release:       1
Summary:       Window and compositing manager based on Clutter
License:       GPLv2+
URL:           https://www.gnome.org
Source0:       %{name}-%{version}.tar.xz

BuildRequires: chrpath pango-devel startup-notification-devel gnome-desktop3-devel
BuildRequires: glib2-devel >= %{glib_ver} gtk3-devel >= %{gtk3_ver}
BuildRequires: gobject-introspection-devel >= 1.41.0 libSM-devel pkgconf-pkg-config
BuildRequires: libwacom-devel libX11-devel libXdamage-devel libXext-devel
BuildRequires: libXfixes-devel libXi-devel libXrandr-devel libXrender-devel
BuildRequires: libXcursor-devel libXcomposite-devel libxcb-devel libxkbcommon-devel
BuildRequires: libxkbcommon-x11-devel libxkbfile-devel libXtst-devel
BuildRequires: mesa-libEGL-devel mesa-libGLES-devel mesa-libGL-devel
BuildRequires: mesa-libgbm-devel pam-devel pipewire-devel >= %{pipewire_ver}
BuildRequires: systemd-devel upower-devel xorg-x11-server-Xorg xkeyboard-config-devel
BuildRequires: zenity desktop-file-utils automake autoconf libtool
%if %{with profiler}
BuildRequires: sysprof-devel
%endif

# Bootstrap requirements
BuildRequires: gtk-doc gnome-common gettext-devel git libcanberra-devel
BuildRequires: gsettings-desktop-schemas-devel >= %{gsettings_desktop_schemas_ver}
BuildRequires: gnome-settings-daemon-devel meson libgudev-devel libdrm-devel 
BuildRequires: libgbm-devel wayland-devel egl-wayland-devel json-glib-devel >= %{json_glib_ver}
BuildRequires: libinput-devel >= %{libinput_ver} xorg-x11-server-Xwayland

Requires:      gnome-control-center-filesystem gtk3 pipewire >= %{pipewire_ver}
Requires:      gsettings-desktop-schemas >= %{gsettings_desktop_schemas_ver}
Requires:      startup-notification dbus zenity json-glib >= %{json_glib_ver}
Requires:      libinput >= %{libinput_ver}

Obsoletes:     mutter-wayland < 3.13.0 mutter-wayland-devel < 3.13.0
Conflicts:     gnome-shell < 3.21.1

%description
Mutter is a window and compositing manager based on Clutter, forked
from Metacity.

%package       devel
Summary:       Development files and Header files for %{name}
Requires:      %{name} = %{version}-%{release}
Provides:      %{name}-tests = %{version}-%{release}
Obsoletes:     %{name}-tests < %{version}-%{release}

%description   devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package_help

%prep
%autosetup -n %{name}-%{version} -p1 

%build
%meson -Degl_device=true -Dwayland_eglstream=true \
%if %{with profiler}
       -Dprofiler=true \
%else
       -Dprofiler=false \
%endif

%meson_build

%install
%meson_install

%find_lang %{name}
desktop-file-validate %{buildroot}/%{_datadir}/applications/%{name}.desktop

%ldconfig_scriptlets

%files -f %{name}.lang
%defattr(-,root,root)
%license COPYING
%{_bindir}/mutter
%{_libdir}/lib*.so.*
%{_libdir}/mutter-%{mutter_api_ver}/
%{_libexecdir}/mutter-restart-helper
%{_datadir}/applications/*.desktop
%{_datadir}/GConf/gsettings/mutter-schemas.convert
%{_datadir}/glib-2.0/schemas/*.gschema.xml
%{_datadir}/gnome-control-center/keybindings/50-mutter-*.xml

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/*
%{_libexecdir}/installed-tests/mutter-%{mutter_api_ver}
%{_datadir}/mutter-%{mutter_api_ver}/tests
%{_datadir}/installed-tests/mutter-%{mutter_api_ver}

%files help
%defattr(-,root,root)
%doc NEWS 
%{_mandir}/man1/mutter.1*

%changelog
* Tue Jan 7 2020 openEuler Buildteam <buildteam@openeuler.org> - 3.34.3-1
- update to 3.34.3

* Mon Dec 9 2019 openEuler Buildteam <buildteam@openeuler.org> - 3.30.1-7
- Type:bugfix
- Id:NA
- SUG:NA
- DESC:modify the files

* Mon Sep 16 2019 openEuler Buildteam <buildteam@openeuler.org> - 3.30.1-6
- Package init
