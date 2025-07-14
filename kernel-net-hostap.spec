#
# Conditional build:
%bcond_without	dist_kernel	# allow non-distribution kernel
%bcond_without	smp		# don't build SMP module
%bcond_with	verbose		# verbose build (V=1)
#
%define		rel	0.1
Summary:	HostAP kernel drivers
Summary(es.UTF-8):	Driveres del núcleo de HostAP
Summary(pl.UTF-8):	Sterowniki HostAP dla jądra Linuksa
Name:		kernel-net-hostap
Version:	0.4.7
Release:	%{rel}@%{_kernel_ver_str}
License:	GPL v2
Group:		Base/Kernel
Source0:	http://hostap.epitest.fi/releases/hostap-driver-%{version}.tar.gz
# Source0-md5:	ee495686cf27011b4e401963c2c7f62a
Patch0:		%{name}-flash.patch
URL:		http://hostap.epitest.fi/
BuildRequires:	%{kgcc_package}
%if %{with dist_kernel}
BuildRequires:	kernel-module-build >= 3:2.6.14
%requires_releq_kernel_up
%endif
BuildRequires:	rpmbuild(macros) >= 1.153
Requires(post,postun):	/sbin/depmod
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
HostAP kernel drivers.

%description -l es.UTF-8
Módulos de núcleo para HostAP.

%description -l pl.UTF-8
Sterowniki HostAP dla jądra Linuksa.

%package -n kernel-pcmcia-net-hostap
Summary:	HostAP PCMCIA kernel drivers
Summary(pl.UTF-8):	Sterowniki HostAP PCMCIA dla jądra Linuksa
Release:	%{rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%{?with_dist_kernel:%requires_releq_kernel_up}
Requires(post,postun):	/sbin/depmod
Requires:	kernel(pcmcia)
Requires:	kernel-net-hostap = %{version}-%{rel}@%{_kernel_ver_str}

%description -n kernel-pcmcia-net-hostap
HostAP PCMCIA kernel drivers.

%description -n kernel-pcmcia-net-hostap -l pl.UTF-8
Sterowniki HostAP PCMCIA dla jądra Linuksa.

%package -n kernel-smp-net-hostap
Summary:	HostAP kernel drivers - SMP version
Summary(es.UTF-8):	Driveres del núcleo de HostAP - versión SMP
Summary(pl.UTF-8):	Sterowniki HostAP dla jądra Linuksa SMP
Release:	%{rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%{?with_dist_kernel:%requires_releq_kernel_smp}
Requires(post,postun):	/sbin/depmod
Provides:	kernel-net-hostap = %{version}-%{rel}@%{_kernel_ver_str}

%description -n kernel-smp-net-hostap
HostAP kernel drivers. SMP version.

%description -n kernel-smp-net-hostap -l es.UTF-8
Módulos de núcleo para HostAP. Versión SMP.

%description -n kernel-smp-net-hostap -l pl.UTF-8
Sterowniki HostAP dla jądra Linuksa SMP.

%package -n kernel-smp-pcmcia-net-hostap
Summary:	HostAP kernel drivers - PCMCIA SMP version
Summary(pl.UTF-8):	Sterowniki HostAP PCMCIA dla jądra Linuksa SMP
Release:	%{rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%{?with_dist_kernel:%requires_releq_kernel_smp}
Requires(post,postun):	/sbin/depmod
Requires:	kernel(pcmcia)
Requires:	kernel-smp-net-hostap = %{version}-%{rel}@%{_kernel_ver_str}

%description -n kernel-smp-pcmcia-net-hostap
HostAP kernel drivers. SMP version.

%description -n kernel-smp-pcmcia-net-hostap -l pl.UTF-8
Sterowniki HostAP PCMCIA dla jądra Linuksa SMP.

%package devel
Summary:	Header files for developing hostap driver based applications
Summary(pl.UTF-8):	Pliki nagłówkowe do bibliotek hostap-driver
Group:		Development/Libraries
# doesn't require kernel modules

%description devel
This package includes the header files necessary to develop
applications that use hostap.

%description devel -l pl.UTF-8
Ten pakiet zawiera pliki nagłówkowe potrzebne do tworzenia aplikacji
używających sterownika hostap.

%prep
%setup -q -n hostap-driver-%{version}
%patch -P0 -p0

%build
# kernel module(s)
cd driver/modules
for cfg in %{?with_dist_kernel:%{?with_smp:smp} up}%{!?with_dist_kernel:nondist}; do
	if [ ! -r "%{_kernelsrcdir}/config-$cfg" ]; then
		exit 1
	fi
	install -d o/include/linux
	ln -sf %{_kernelsrcdir}/config-$cfg o/.config
	ln -sf %{_kernelsrcdir}/Module.symvers-$cfg o/Module.symvers
	ln -sf %{_kernelsrcdir}/include/linux/autoconf-$cfg.h o/include/linux/autoconf.h
%if %{with dist_kernel}
	%{__make} -j1 -C %{_kernelsrcdir} O=$PWD/o prepare scripts
%else
	install -d o/include/config
	touch o/include/config/MARKER
	ln -sf %{_kernelsrcdir}/scripts o/scripts
%endif
#
#	patching/creating makefile(s) (optional)
#
	%{__make} -C %{_kernelsrcdir} clean \
		RCS_FIND_IGNORE="-name '*.ko' -o" \
		SYSSRC=%{_kernelsrcdir} \
		SYSOUT=$PWD/o \
		M=$PWD O=$PWD/o \
		%{?with_verbose:V=1}
	%{__make} -C %{_kernelsrcdir} modules \
		CC="%{__cc}" CPP="%{__cpp}" \
		SYSSRC=%{_kernelsrcdir} \
		SYSOUT=$PWD/o \
		M=$PWD O=$PWD/o \
		%{?with_verbose:V=1}
	mkdir -p built/$cfg
	mv hostap*.ko built/$cfg/
done

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}{,smp}/kernel/drivers/net/{pcmcia,wireless}
install -d $RPM_BUILD_ROOT%{_sysconfdir}/pcmcia
install -d $RPM_BUILD_ROOT%{_includedir}

install driver%{_sysconfdir}/hostap_cs.conf \
	$RPM_BUILD_ROOT%{_sysconfdir}/pcmcia

cd driver/modules/built
install %{?with_dist_kernel:up}%{!?with_dist_kernel:nondist}/hostap{,_crypt*,_pci}.ko \
	$RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/kernel/drivers/net/wireless
install %{?with_dist_kernel:up}%{!?with_dist_kernel:nondist}/hostap{_cs,_plx}.ko \
	$RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/kernel/drivers/net/pcmcia
%if %{with smp} && %{with dist_kernel}
install smp/hostap{,_crypt*,_pci}.ko \
	$RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp/kernel/drivers/net/wireless
install smp/hostap{_cs,_plx}.ko \
	$RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp/kernel/drivers/net/pcmcia
%endif
install ../*.h $RPM_BUILD_ROOT%{_includedir}

%post
%depmod %{_kernel_ver}

%preun
%depmod %{_kernel_ver}

%post -n kernel-pcmcia-net-hostap
%depmod %{_kernel_ver}

%postun -n kernel-pcmcia-net-hostap
%depmod %{_kernel_ver}

%post -n kernel-smp-net-hostap
%depmod %{_kernel_ver}smp

%postun -n kernel-smp-net-hostap
%depmod %{_kernel_ver}smp

%post -n kernel-smp-pcmcia-net-hostap
%depmod %{_kernel_ver}smp

%postun -n kernel-smp-pcmcia-net-hostap
%depmod %{_kernel_ver}smp

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc ChangeLog README
/lib/modules/%{_kernel_ver}/kernel/drivers/net/wireless/*.ko*

%ifnarch sparc sparc64
%files -n kernel-pcmcia-net-hostap
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcmcia/hostap_cs.conf
/lib/modules/%{_kernel_ver}/kernel/drivers/net/pcmcia/*.ko*
%endif

%if %{with smp} && %{with dist_kernel}
%files -n kernel-smp-net-hostap
%defattr(644,root,root,755)
%doc ChangeLog README
/lib/modules/%{_kernel_ver}smp/kernel/drivers/net/wireless/*.ko*

%ifnarch sparc sparc64
%files -n kernel-smp-pcmcia-net-hostap
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcmcia/hostap_cs.conf
/lib/modules/%{_kernel_ver}smp/kernel/drivers/net/pcmcia/*.ko*
%endif
%endif

%files devel
%defattr(644,root,root,755)
%{_includedir}/*.h
