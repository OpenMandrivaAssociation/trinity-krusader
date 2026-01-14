%bcond clang 1

# TDE variables
%define tde_epoch 2
%if "%{?tde_version}" == ""
%define tde_version 14.1.5
%endif
%define pkg_rel 2

%define tde_pkg krusader
%define tde_prefix /opt/trinity


%undefine __brp_remove_la_files
%define dont_remove_libtool_files 1
%define _disable_rebuild_configure 1

%define tarball_name %{tde_pkg}-trinity


Name:		trinity-%{tde_pkg}
Epoch:		%{tde_epoch}
Version:	1.90.0
Release:	%{?tde_version}_%{?!preversion:%{pkg_rel}}%{?preversion:0_%{preversion}}%{?dist}
Summary:	Twin-panel (commander-style) file manager for TDE (and other desktops)
Group:		Applications/Utilities
URL:		http://www.trinitydesktop.org/

License:	GPLv2+


Source0:		https://mirror.ppa.trinitydesktop.org/trinity/releases/R%{tde_version}/main/applications/system/%{tarball_name}-%{tde_version}%{?preversion:~%{preversion}}.tar.xz

BuildRequires:	trinity-tdelibs-devel >= %{tde_version}
BuildRequires:	trinity-tdebase-devel >= %{tde_version}
BuildRequires:	desktop-file-utils
BuildRequires:	trinity-tdebindings-devel >= %{tde_version}

BuildRequires:	autoconf automake libtool m4 make

%{!?with_clang:BuildRequires:	gcc-c++}

BuildRequires:	pkgconfig
BuildRequires:	fdupes

BuildRequires:  pkgconfig(xrender)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(ice)
BuildRequires:  pkgconfig(sm)
BuildRequires:  pkgconfig(xext)
BuildRequires:  pkgconfig(xi)
BuildRequires:  pkgconfig(xrandr)
BuildRequires:  pkgconfig(xcursor)
BuildRequires:  pkgconfig(xinerama)
BuildRequires:  pkgconfig(xft)


%description
Krusader is a simple, easy, powerful, twin-panel (commander-style) file
manager for TDE and other desktops, similar to Midnight Commander (C) or Total
Commander (C).

It provides all the file management features you could possibly want.

Plus: extensive archive handling, mounted filesystem support, FTP,
advanced search module, viewer/editor, directory synchronisation,
file content comparisons, powerful batch renaming and much much more.

It supports archive formats: ace, arj, bzip2, deb, iso, lha, rar, rpm, tar,
zip and 7-zip.

It handles KIOSlaves such as smb:// or fish://.

Almost completely customizable, Krusader is very user friendly, fast and looks
great on your desktop.


%prep
%autosetup -n %{tarball_name}-%{tde_version}%{?preversion:~%{preversion}}

%__cp "/usr/share/aclocal/libtool.m4" "admin/libtool.m4.in"
%__cp -f "/usr/share/libtool/config/ltmain.sh" "admin/ltmain.sh" || %__cp -f "/usr/share/libtool/"*"/ltmain.sh" "admin/ltmain.sh" || %__cp -f "/usr/share/libtool/ltmain.sh" "admin/ltmain.sh"
%__make -f "admin/Makefile.common"


%build
unset QTDIR QTINC QTLIB
export PATH="%{tde_prefix}/bin:${PATH}"

# Warning: --enable-final causes FTBFS
%configure \
  --prefix=%{tde_prefix} \
  --exec-prefix=%{tde_prefix} \
  --bindir=%{tde_prefix}/bin \
  --datadir=%{tde_prefix}/share \
  --libdir=%{tde_prefix}/%{_lib} \
  --mandir=%{tde_prefix}/share/man \
  --includedir=%{tde_prefix}/include/tde \
  \
  --disable-dependency-tracking \
  --disable-debug \
  --enable-new-ldflags \
  --disable-final \
  --enable-closure \
  --enable-rpath \
  --disable-gcc-hidden-visibility

%__make %{?_smp_mflags}


%install
export PATH="%{tde_prefix}/bin:${PATH}"
%__make install DESTDIR=%{buildroot}

%find_lang %{tde_pkg}


%files -f %{tde_pkg}.lang
%defattr(-,root,root,-)
%doc AUTHORS COPYING FAQ README TODO
%{tde_prefix}/bin/krusader
%{tde_prefix}/%{_lib}/trinity/tdeio_krarc.la
%{tde_prefix}/%{_lib}/trinity/tdeio_krarc.so
%{tde_prefix}/%{_lib}/trinity/tdeio_virt.la
%{tde_prefix}/%{_lib}/trinity/tdeio_virt.so
%{tde_prefix}/share/applications/tde/krusader.desktop
%{tde_prefix}/share/applications/tde/krusader_root-mode.desktop
%{tde_prefix}/share/apps/krusader
%{tde_prefix}/share/apps/tdeconf_update/krusader_tqt_selection.upd
%{tde_prefix}/share/icons/crystalsvg/*/apps/*.png
%{tde_prefix}/share/icons/locolor/*/apps/*.png
%{tde_prefix}/share/services/krarc.protocol
%{tde_prefix}/share/services/virt.protocol
%{tde_prefix}/share/man/man1/krusader.1
%{tde_prefix}/share/doc/tde/HTML/en/krusader/
%{tde_prefix}/share/doc/tde/HTML/en/tdeioslave/krarc/
%{tde_prefix}/share/doc/tde/HTML/en/tdeioslave/virt/
%lang(ru) %{tde_prefix}/share/doc/tde/HTML/ru/krusader/

