Name:          mutter
Version:       3.38.4
Release:       4
Summary:       Window and compositing manager based on Clutter
License:       GPLv2+
URL:           https://www.gnome.org
Source0:       https://download.gnome.org/sources/%{name}/3.38/%{name}-%{version}.tar.xz

Patch0:        0001-window-actor-Special-case-shaped-Java-windows.patch

BuildRequires: startup-notification-devel gnome-desktop3-devel 
BuildRequires: gobject-introspection-devel libSM-devel libwacom-devel 
BuildRequires: libxkbcommon-x11-devel libxkbfile-devel 
BuildRequires: mesa-libEGL-devel mesa-libGL-devel mesa-libgbm-devel 
BuildRequires: desktop-file-utils 
BuildRequires: libcanberra-devel json-glib-devel 
BuildRequires: libinput-devel 
BuildRequires: pkgconfig(graphene-gobject-1.0) pkgconfig(libpipewire-0.3) >= 0.3.0
BuildRequires: gnome-settings-daemon-devel meson
BuildRequires: pkgconfig(wayland-eglstream) xorg-x11-server-Xwayland
%ifarch riscv64
BuildRequires: pkgconfig(libdrm)
BuildRequires: pkgconfig(sysprof-capture-4)
%endif

Obsoletes:     mutter-wayland < 3.13.0
Obsoletes:     mutter-wayland-devel < 3.13.0

Conflicts:     gnome-shell < 3.21.1

Requires:      gnome-control-center-filesystem libinput gsettings-desktop-schemas
Requires:      gtk3 pipewire startup-notification dbus-x11 zenity json-glib
Requires:      gsettings-desktop-schemas

%description
Mutter is a window and compositing manager based on Clutter, forked
from Metacity.

%package       devel
Summary:       Development files and Header files for %{name}
Requires:      %{name} = %{version}-%{release}
Provides:      %{name}-tests
Obsoletes:     %{name}-tests < %{version}-%{release}
%description   devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package_help

%prep
%autosetup -n %{name}-%{version} -p1 

%build
%meson -Degl_device=true -Dwayland_eglstream=true -Dxwayland_initfd=disabled
%meson_build

%install
%meson_install
%delete_la_and_a

%find_lang %{name}

desktop-file-validate %{buildroot}/%{_datadir}/applications/%{name}.desktop

mkdir -p %{buildroot}/etc/ld.so.conf.d
echo "/usr/lib64/mutter-7" > %{buildroot}/etc/ld.so.conf.d/%{name}-%{_arch}.conf
%ldconfig_scriptlets

%files -f %{name}.lang
%defattr(-,root,root)
%license COPYING
%config(noreplace) /etc/ld.so.conf.d/%{name}-%{_arch}.conf
%{_bindir}/mutter
%{_libdir}/mutter-7/*
%{_libdir}/libmutter-7.so.*
%{_prefix}/libexec/mutter-restart-helper
%{_datadir}/applications/*.desktop
%{_datadir}/glib-2.0/schemas/*.gschema.xml
%{_datadir}/GConf/gsettings/mutter-schemas.convert
%{_datadir}/gnome-control-center/keybindings/50-mutter*
%{_prefix}/lib/udev/rules.d/61-mutter.rules

%files  devel
%defattr(-,root,root)
%{_bindir}/*
%{_includedir}/mutter-7/*
%{_libdir}/pkgconfig/*.pc
%{_libdir}/libmutter-7.so
%{_prefix}/libexec/installed-tests/*
%{_datadir}/installed-tests/*
%{_datadir}/mutter-7/tests/stacking/*.metatest

%files help
%defattr(-,root,root)
%doc NEWS 
%{_mandir}/man1/*.1.gz

%changelog
* Wed Jan 12 2022 lvxiaoqian <xiaoqian@nj.iscas.ac.cn> - 3.38.4-4
- add BuildRequires for riscv

* Tue Sep 16 2021 weijin deng <weijin.deng@turbolinux.com.cn> - 3.38.4-3
- Add concrete dynamic library search path

* Wed Aug 25 2021 chenyanpanHW <chenyanpan@huawei.com> - 3.38.4-2
- DESC: remove unnecessary BuildRequires

* Mon May 31 2021 weijin deng <weijin.deng@turbolinux.com.cn> - 3.38.4-1
- Upgrade to 3.38.4
- Update Version, Release, BuildRequires, Obsoletes
- Delete patches which existed in new version, add one patch
- Use meson rebuild. update stage 'install', 'files'

* Wed Aug 5 2020 orange-snn <songnannan2@huawei.com> - 3.30.1-8
- change mesa-libEGL-devel to libglvnd-devel in buildrequires

* Mon Dec 9 2019 openEuler Buildteam <buildteam@openeuler.org> - 3.30.1-7
- Type:bugfix
- Id:NA
- SUG:NA
- DESC:modify the files

* Mon Sep 16 2019 openEuler Buildteam <buildteam@openeuler.org> - 3.30.1-6
- Package init

