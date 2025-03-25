# TODO: system cpuinfo (when released? note: different project than packaged in cpuinfo.spec)
Summary:	Scalable Video Technology for JPEG-XS (SVT-JPEG-XS Encoder and Decoder)
Summary(pl.UTF-8):	Scalable Video Technology dla JPEG-XS (koder i dekoder SVT-JPEG-XS)
Name:		svt-jpeg-xs
Version:	0.9.0
Release:	1
License:	BSD
Group:		Libraries
#Source0Download: https://github.com/OpenVisualCloud/SVT-JPEG-XS/releases
Source0:	https://github.com/OpenVisualCloud/SVT-JPEG-XS/archive/v%{version}/SVT-JPEG-XS-%{version}.tar.gz
# Source0-md5:	c9d92f9158927698e074d3658464952f
Patch0:		%{name}-no-asm.patch
URL:		https://github.com/OpenVisualCloud/SVT-JPEG-XS
BuildRequires:	cmake >= 3.5
BuildRequires:	libstdc++-devel >= 6:4.7
BuildRequires:	rpmbuild(macros) >= 1.605
%ifarch %{x8664}
# preferred by cmake; also nasm >= 2.13 possible
BuildRequires:	yasm >= 1.2.0
%endif
# other archs can be supported by removing ARCH_X86_64 define (which enables SIMD support via gcc intrinsics)
ExclusiveArch:	%{ix86} %{x8664} x32
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This library is implementation of ISO/IEC 21122 protocol.

%description -l pl.UTF-8
Ta biblioteka to implementacja protokołu ISO/IEC 21122.

%package devel
Summary:	Header files for SVT-JPEG-XS library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki SVT-JPEG-XS
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for SVT-JPEG-XS library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki SVT-JPEG-XS.

%prep
%setup -q -n SVT-JPEG-XS-%{version}
%patch -P0 -p1

%build
install -d build
cd build
%cmake .. \
%ifnarch %{x8664}
	-DDISABLE_ASM=ON
%endif

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc LICENSE.md README.md 
%attr(755,root,root) %{_bindir}/SvtJpegxsDecApp
%attr(755,root,root) %{_bindir}/SvtJpegxsEncApp
%attr(755,root,root) %{_bindir}/SvtJpegxsSampleDecoder
%attr(755,root,root) %{_bindir}/SvtJpegxsSampleEncoder
%attr(755,root,root) %{_libdir}/libSvtJpegxs.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libSvtJpegxs.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libSvtJpegxs.so
%{_includedir}/svt-jpegxs
%{_pkgconfigdir}/SvtJpegxs.pc
