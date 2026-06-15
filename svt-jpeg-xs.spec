# TODO: system cpuinfo (when released? note: different project than packaged in cpuinfo.spec)
# NOTE: snapshot of the main branch - upstream has not tagged 0.10.0 yet, but
# ffmpeg >= 8.1 requires SvtJpegxs >= 0.10.0 (the 0.9.0 release reports 0.9.0
# and fails ffmpeg's pkg-config check). Switch Source0 back to a release tag
# once upstream tags 0.10.0.
%define		gitcommit	8e50180ad909a0bdcdf91b462c64033f0fe3e112
%define		gitshort	%(echo %{gitcommit} | cut -c1-7)
Summary:	Scalable Video Technology for JPEG-XS (SVT-JPEG-XS Encoder and Decoder)
Summary(pl.UTF-8):	Scalable Video Technology dla JPEG-XS (koder i dekoder SVT-JPEG-XS)
Name:		svt-jpeg-xs
Version:	0.10.0
Release:	0.20260519.1
License:	BSD
Group:		Libraries
#Source0Download: https://github.com/OpenVisualCloud/SVT-JPEG-XS/releases
Source0:	https://github.com/OpenVisualCloud/SVT-JPEG-XS/archive/%{gitcommit}/%{name}-%{version}-%{gitshort}.tar.gz
# Source0-md5:	b735f2f34642e05d7c3c0f4084d90110
Patch0:		%{name}-no-asm.patch
URL:		https://github.com/OpenVisualCloud/SVT-JPEG-XS
BuildRequires:	cmake >= 3.10
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
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for SVT-JPEG-XS library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki SVT-JPEG-XS.

%prep
%setup -q -n SVT-JPEG-XS-%{gitcommit}
%patch -P0 -p1

%build
%cmake -B build \
%ifnarch %{x8664}
	-DDISABLE_ASM=ON
%endif

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
