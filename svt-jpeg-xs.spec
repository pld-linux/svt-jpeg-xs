# TODO: system cpuinfo (when released? note: different project than packaged in cpuinfo.spec)
Summary:	Scalable Video Technology for JPEG-XS (SVT-JPEG-XS Encoder and Decoder)
Summary(pl.UTF-8):	Scalable Video Technology dla JPEG-XS (koder i dekoder SVT-JPEG-XS)
Name:		svt-jpeg-xs
Version:	0.10.0
Release:	1
License:	BSD
Group:		Libraries
#Source0Download: https://github.com/OpenVisualCloud/SVT-JPEG-XS/releases
Source0:	https://github.com/OpenVisualCloud/SVT-JPEG-XS/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	319ec50626486089ec20fa171d332658
Patch0:		%{name}-no-asm.patch
URL:		https://github.com/OpenVisualCloud/SVT-JPEG-XS
BuildRequires:	cmake >= 3.13
BuildRequires:	libstdc++-devel >= 6:4.7
BuildRequires:	rpmbuild(macros) >= 1.605
%ifarch %{x8664}
# preferred by cmake; also yasm >= 1.2.0 possible
BuildRequires:	nasm >= 2.14
%endif
# other archs can be supported by removing ARCH_X86_64 define (which enables SIMD support via gcc intrinsics)
ExclusiveArch:	%{ix86} %{x8664} x32
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# it defines -D_FORTIFY_SOURCE=3 on its own (as of 0.10.0)
%define		filterout_c	-Wp,-D_FORTIFY_SOURCE=2

%description
SVT-JPEG-XS (Scalable Video Technology for JPEG-XS) is an open-source
JPEG-XS (ISO/IEC 21122) encoder and decoder library optimized for
Intel architectures. JPEG-XS is a low-latency, visually lossless
intra-frame codec for professional video transport.

%description -l pl.UTF-8
SVT-JPEG-XS (Scalable Video Technology dla JPEG-XS) to otwarta
biblioteka kodera i dekodera JPEG-XS (ISO/IEC 21122), zoptymalizowana
pod kątem architektur Intela. JPEG-XS to wewnątrzklatkowy kodek o
małych opóźnieniach i wizualnie bezstratnej jakości, przeznaczony do
profesjonalnego przesyłania obrazu.

%package devel
Summary:	Header files for SVT-JPEG-XS library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki SVT-JPEG-XS
Group:		Development/Libraries
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description devel
Header files for SVT-JPEG-XS library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki SVT-JPEG-XS.

%prep
%setup -q -n SVT-JPEG-XS-%{version}
%patch -P0 -p1

%build
%cmake -B build

%{__make} -C build

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
%{_libdir}/libSvtJpegxs.so.*.*.*
%ghost %{_libdir}/libSvtJpegxs.so.0

%files devel
%defattr(644,root,root,755)
%{_libdir}/libSvtJpegxs.so
%{_includedir}/svt-jpegxs
%{_pkgconfigdir}/SvtJpegxs.pc
