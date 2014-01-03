# NOTE: this spec contains the last glfw 2.x for backward compatibility,
# built as parallel-installable with glfw 3.x.
# The only change required at build time is to change "-lglfw" to "-lglfw2".
Summary:	Free, portable framework for OpenGL application development
Summary(pl.UTF-8):	Wolnodostępny, przenośny szkielet do tworzenia aplikacji OpenGL
Name:		glfw2
Version:	2.7.9
Release:	1
License:	BSD-like
Group:		Libraries
Source0:	http://downloads.sourceforge.net/glfw/glfw-%{version}.tar.bz2
# Source0-md5:	96e12be48801984f0f0c23e38549b277
Patch0:		%{name}-opt.patch
Patch1:		%{name}-libdir.patch
Patch2:		%{name}-soname.patch
URL:		http://glfw.sourceforge.net/
BuildRequires:	OpenGL-GLU-devel
BuildRequires:	OpenGL-GLX-devel
BuildRequires:	libtool
BuildRequires:	sed >= 4.0
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-lib-libXxf86vm-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
GLFW is a free, Open Source, portable framework for OpenGL application
development. In short, it is a single library providing a powerful,
portable API for otherwise operating system specific tasks such as
opening an OpenGL window, and reading keyboard, mouse and joystick
input.

It also provides functions for reading a high precision timer,
accessing OpenGL extensions, creating and synchronizing threads,
reading textures from files and more.

GLFW is available for Windows, MacOS X, Unix-like systems such as
Linux and FreeBSD, and for AmigaOS and DOS.

%description -l pl.UTF-8
GLFW to wolnodostępny, mający otwarte źródła, przenośny szkielet do
tworzenia aplikacji OpenGL. W skrócie jest to pojedyncza biblioteka
udostępniająca potężne, przenośne API do zadań zależnych od systemu
operacyjnego, takich jak otwieranie okna OpenGL, odczyt wejścia z
klawiatury, myszy i joysticka.

Zawiera także funkcje do odczytu zegara o wysokiej rozdzielczości,
dostępu do rozszerzeń OpenGL, tworzenia i synchronizowania wątków,
odczytu tekstur z plików i innych zadań.

GLFW jest dostępny dla Windows, MacOS X, systemów uniksowych takich
jak Linux czy FreeBSD oraz dla AmigaOS i DOS-a.

%package devel
Summary:	Header files for GLFW 2 library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki GLFW 2
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	OpenGL-GLX-devel
Requires:	xorg-lib-libX11-devel
Requires:	xorg-lib-libXxf86vm-devel

%description devel
Header files for GLFW 2 library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki GLFW 2.

%package static
Summary:	Static GLFW 2 library
Summary(pl.UTF-8):	Statyczna biblioteka GLFW 2
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static GLFW 2 library.

%description static -l pl.UTF-8
Statyczna biblioteka GLFW 2.

%prep
%setup -q -n glfw-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
CC="%{__cc}" \
LFLAGS="%{rpmldflags}" \
CFLAGS="%{rpmcflags}" \
sh ./compile.sh

%{__make} -C lib/x11 -f Makefile.x11 \
	PREFIX=%{_prefix} \
	LIBDIR=%{_libdir}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%{__make} -C lib/x11 -f Makefile.x11 dist-install \
	DESTDIR=$RPM_BUILD_ROOT \
	PREFIX=%{_prefix} \
	LIBDIR=%{_libdir}

install examples/{*.c,*.tga,Makefile.x11} $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

# make it parallel-installable with glfw 3.x (from glfw.spec)
%{__mv} $RPM_BUILD_ROOT%{_libdir}/{libglfw.so,libglfw.so.%{version}}
ln -sf libglfw.so.%{version} $RPM_BUILD_ROOT%{_libdir}/libglfw.so.2
ln -sf libglfw.so.%{version} $RPM_BUILD_ROOT%{_libdir}/libglfw2.so
%{__mv} $RPM_BUILD_ROOT%{_libdir}/{libglfw.a,libglfw2.a}
%{__sed} -i -e 's,-lglfw,-lglfw2,' $RPM_BUILD_ROOT%{_pkgconfigdir}/libglfw.pc

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc COPYING.txt readme.html
%attr(755,root,root) %{_libdir}/libglfw.so.2.*.*
%attr(755,root,root) %ghost %{_libdir}/libglfw.so.2

%files devel
%defattr(644,root,root,755)
%doc docs/{Reference,UsersGuide}.pdf
%attr(755,root,root) %{_libdir}/libglfw2.so
%{_includedir}/GL/glfw.h
%{_pkgconfigdir}/libglfw.pc
%{_examplesdir}/%{name}-%{version}

%files static
%defattr(644,root,root,755)
%{_libdir}/libglfw2.a
