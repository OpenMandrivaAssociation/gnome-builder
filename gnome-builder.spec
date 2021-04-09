# "fix" lua underlinking:
%define _disable_ld_no_undefined 1

%define url_ver %(echo %{version}|cut -d. -f1,2)

# python are templates which cannot be byte compiled
%define _python_bytecompile_build 0

# filter out plugin .so from provides
# Exclude privlibs
%global privlibs .*-private|libide|libgnome-builder-plugins
%global __requires_exclude ^(%{privlibs}).*\\.so.*
%global __provides_exclude_from %{_libdir}/gnome-builder/plugins/.*\\.so

%global libpeas_version 1.22.0
%global jsonrpc_glib_version 3.26.1

Name:		gnome-builder
Version:	3.40.0
Release:	1
Summary:	IDE for writing GNOME-based software
License:	GPLv2+
Group:		Graphical desktop/GNOME
URL:		https://wiki.gnome.org/Apps/Builder
Source0:	https://download.gnome.org/sources/%{name}/%{url_ver}/%{name}-%{version}.tar.xz
Patch0:		work-around-wshadow-error.patch
BuildRequires:	bison
BuildRequires:	intltool
BuildRequires:	appstream-util
BuildRequires:	clang-devel
BuildRequires:	docbook-style-xsl
BuildRequires:	flex
BuildRequires:	gsettings-desktop-schemas
BuildRequires:	itstool
BuildRequires:	libxml2-utils
BuildRequires:	llvm-devel
BuildRequires:	meson
BuildRequires:	pkgconfig(enchant-2)
BuildRequires:	pkgconfig(flatpak)
BuildRequires:	pkgconfig(gjs-1.0) >= 1.42.0
BuildRequires:	pkgconfig(gobject-introspection-1.0) >= 1.35.9
BuildRequires:	pkgconfig(gspell-1)
BuildRequires:	pkgconfig(gtk+-3.0) >= 3.9.6
BuildRequires:	pkgconfig(gtksourceview-4)
BuildRequires:	pkgconfig(json-glib-1.0)
BuildRequires:  pkgconfig(jsonrpc-glib-1.0) >= %{jsonrpc_glib_version}
BuildRequires:  pkgconfig(libdazzle-1.0)
BuildRequires:	pkgconfig(libdevhelp-3.0)
BuildRequires:	pkgconfig(libgit2-glib-1.0)
BuildRequires:  pkgconfig(libpeas-1.0) >= %{libpeas_version}
BuildRequires:  pkgconfig(libpcre2-8)
BuildRequires:  pkgconfig(libportal)
BuildRequires:	pkgconfig(mm-common-util)
BuildRequires:	pkgconfig(pygobject-3.0) >= 3.0.0
BuildRequires:	pkgconfig(python)
BuildRequires:	pkgconfig(sysprof-ui-4) >= 3.29.3
BuildRequires:	pkgconfig(systemd)
BuildRequires:  pkgconfig(template-glib-1.0)
BuildRequires:	pkgconfig(vapigen)
BuildRequires:	pkgconfig(vte-2.91)
BuildRequires:	python-gobject3
BuildRequires:	vala-tools
BuildRequires:  vala
BuildRequires:	xsltproc
BuildRequires:  pkgconfig(gladeui-2.0)
BuildConflicts: valgrind-devel <= 3.13.0-10.mga7

Requires:	gtksourceview >= 4
Requires:	gsettings-desktop-schemas
# Not imported yet for Cooker (penguin)
#Requires:	pythonegg(3)(jedi)

Recommends:	flatpak-builder
Recommends:     clang
Recommends:     gnome-code-assistance
Recommends:     meson
Recommends:     python3-jedi

%description
Builder attempts to be an IDE for writing software for GNOME. It does not try
to be a generic IDE, but one specialized for writing GNOME software.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%autosetup -p1

%build
%global build_ldflags %{build_ldflags} -Wl,-z,notext
#global ldflags %{ldflags} -Wl,-z,notext
#global ldflags %{ldflags} -fuse-ld=gold
# penguin - build error with clang, switch to gcc
#export CC=gcc
#export CXX=g++
%meson -Denable_gtk_doc=true
%meson_build

%install
%meson_install
%find_lang %{name}

%files -f %{name}.lang
%doc NEWS README.md
%license COPYING
%{_bindir}/*
%{_libdir}/%{name}/
%{_libexecdir}/gnome-builder-clang
%{_datadir}/applications/org.gnome.Builder.desktop
%{_datadir}/glib-2.0/schemas/*.xml
%{_iconsdir}/*/*/*/*
%{_datadir}/dbus-1/services/org.gnome.Builder.service
%{_datadir}/gtksourceview-4/*
#{_datadir}/gtksourceview-3.0/styles/builder-dark.style-scheme.xml
#{_datadir}/gtksourceview-3.0/styles/builder.style-scheme.xml
%{_datadir}/gnome-builder
%{_datadir}/metainfo/org.gnome.Builder.appdata.xml
%{python_sitelib}/gi/overrides/Ide.py
%{_libexecdir}/gnome-builder-git
#{_libexecdir}/gnome-builder-vala

%files devel
%{_libdir}/%{name}/pkgconfig/
%{_datadir}/%{name}/gir-1.0/
#{_datadir}/%{name}/vapi/
%{_includedir}/gnome-builder*/

