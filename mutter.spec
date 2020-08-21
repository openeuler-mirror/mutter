Name:          mutter
Version:       3.30.1
Release:       8
Summary:       Window and compositing manager based on Clutter
License:       GPLv2+
URL:           https://www.gnome.org
Source0:       https://download.gnome.org/sources/%{name}/3.30/%{name}-%{version}.tar.xz

# These patchs are from fedora29
# Fix slow startup notification on wayland
Patch0:        startup-notification.patch
# Don't use switch-config when ensuring configuration
Patch1:        0001-monitor-manager-Don-t-use-switch-config-when-ensurin.patch
# Make current placement rule stack allocated
Patch2:        0001-constraints-Make-current-placement-rule-stack-alloca.patch
# Clean up texture regions
Patch3:        0002-shaped-texture-Clean-up-texture-regions.patch
# Defer text_input.done on an idle
Patch4:        0001-wayland-Defer-text_input.done-on-an-idle.patch
# Ignore text-input state commit when not focused
Patch5:        0001-wayland-text-input-Ignore-text-input-state-commit-wh.patch

BuildRequires: chrpath pango-devel startup-notification-devel gnome-desktop3-devel glib2-devel gtk3-devel git
BuildRequires: gobject-introspection-devel libSM-devel libwacom-devel libX11-devel libXdamage-devel libXext-devel
BuildRequires: libXfixes-devel libXi-devel libXrandr-devel libXrender-devel libXcursor-devel libXcomposite-devel
BuildRequires: libxcb-devel libxkbcommon-devel libxkbcommon-x11-devel libxkbfile-devel libXtst-devel systemd-devel
BuildRequires: mesa-libEGL-devel mesa-libGLES-devel mesa-libGL-devel mesa-libgbm-devel pam-devel pipewire-devel
BuildRequires: upower-devel xkeyboard-config-devel zenity desktop-file-utils gtk-doc gnome-common gettext-devel 
BuildRequires: libcanberra-devel gsettings-desktop-schemas-devel automake autoconf libtool json-glib-devel pkgconfig
BuildRequires: libgudev-devel libinput-devel wayland-devel pkgconf-pkg-config libdrm-devel egl-wayland-devel

Obsoletes:     mutter-wayland
Obsoletes:     mutter-wayland-devel

Conflicts:     gnome-shell < 3.21.1

Requires:      gnome-control-center-filesystem libinput gsettings-desktop-schemas
Requires:      gtk3 pipewire startup-notification dbus-x11 zenity json-glib

%description
Mutter is a window and compositing manager based on Clutter, forked
from Metacity.

%package       devel
Summary:       Development files and Header files for %{name}
Requires:      %{name} = %{version}-%{release}
Provides:      %{name}-tests
Obsoletes:     %{name}-tests
%description   devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package_help

%prep
%autosetup -n %{name}-%{version} -p1 

%build
autoreconf -if
(if ! test -x configure; then NOCONFIGURE=1 ./autogen.sh; fi;
 %configure  --enable-compile-warnings=maximum --enable-remote-desktop --enable-installed-tests --with-libwacom --enable-egl-device)

%make_build

%install
%make_install
%delete_la_and_a
desktop-file-validate %{buildroot}/%{_datadir}/applications/%{name}.desktop

%ldconfig_scriptlets

%files 
%defattr(-,root,root)
%license COPYING
%{_bindir}/mutter
%{_libdir}/mutter/*
%{_libdir}/libmutter-3.so.*
%{_prefix}/libexec/mutter-restart-helper
%{_datadir}/locale/*
%{_datadir}/applications/*.desktop
%{_datadir}/glib-2.0/schemas/*.gschema.xml
%{_datadir}/GConf/gsettings/mutter-schemas.convert
%{_datadir}/gnome-control-center/keybindings/50-mutter*

%files  devel
%defattr(-,root,root)
%{_bindir}/*
%{_includedir}/mutter/*
%{_libdir}/pkgconfig/*.pc
%{_libdir}/libmutter-3.so
%{_prefix}/libexec/installed-tests/*
%{_datadir}/installed-tests/*
%{_datadir}/mutter/tests/stacking/*.metatest

%files help
%defattr(-,root,root)
%doc NEWS 
%{_mandir}/man1/*.1.gz

%changelog
* Fri Aug 21 2020 lunankun <lunankun@huawei.com> - 3.30.1-8
- Type:bugfix
- Id:NA
- SUG:NA
- DESC:release +1 for rebuild

* Mon Dec 9 2019 openEuler Buildteam <buildteam@openeuler.org> - 3.30.1-7
- Type:bugfix
- Id:NA
- SUG:NA
- DESC:modify the files

* Mon Sep 16 2019 openEuler Buildteam <buildteam@openeuler.org> - 3.30.1-6
- Package init

