#
# Conditional build:
%bcond_without	dist_kernel	# allow non-distribution kernel
%bcond_without	smp		# don't build SMP module
%bcond_with	verbose		# verbose build (V=1)
#
Summary:	HostAP kernel drivers
Summary(es):	Driveres del núcleo de HostAP
Summary(pl):	Sterowniki HostAP dla j±dra Linuksa
Name:		kernel-net-hostap
Version:	0.2.4
%define		rel	1
Release:	%{rel}@%{_kernel_ver_str}
License:	GPL v2
Group:		Base/Kernel
Source0:	http://hostap.epitest.fi/releases/hostap-driver-%{version}.tar.gz
# Source0-md5:	342f0c94072e90c9a5d775f6e68532af
URL:		http://hostap.epitest.fi/
BuildRequires:	%{kgcc_package}
%if %{with dist_kernel}
BuildRequires:	kernel-module-build >= 2.6.7
%requires_releq_kernel_up
%endif
BuildRequires:	rpmbuild(macros) >= 1.153
Requires(post,postun):	/sbin/depmod
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
HostAP kernel drivers.

%description -l es
Módulos de núcleo para HostAP.

%description -l pl
Sterowniki HostAP dla j±dra Linuksa.

%package -n kernel-pcmcia-net-hostap
Summary:	HostAP PCMCIA kernel drivers
Summary(pl):	Sterowniki HostAP PCMCIA dla j±dra Linuksa
Release:	%{rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%{?with_dist_kernel:%requires_releq_kernel_up}
Requires(post,postun):	/sbin/depmod
Requires:	kernel(pcmcia)
Requires:	kernel-net-hostap = %{version}-%{rel}@%{_kernel_ver_str}

%description -n kernel-pcmcia-net-hostap
HostAP PCMCIA kernel drivers.

%description -n kernel-pcmcia-net-hostap -l pl
Sterowniki HostAP PCMCIA dla j±dra Linuksa.

%package -n kernel-smp-net-hostap
Summary:	HostAP kernel drivers - SMP version
Summary(es):	Driveres del núcleo de HostAP - versión SMP
Summary(pl):	Sterowniki HostAP dla j±dra Linuksa SMP
Release:	%{rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%{?with_dist_kernel:%requires_releq_kernel_smp}
Requires(post,postun):	/sbin/depmod
Provides:	kernel-net-hostap = %{version}-%{rel}@%{_kernel_ver_str}

%description -n kernel-smp-net-hostap
HostAP kernel drivers. SMP version.

%description -n kernel-net-hostap -l es
Módulos de núcleo para HostAP. Versión SMP.

%description -n kernel-smp-net-hostap -l pl
Sterowniki HostAP dla j±dra Linuksa SMP.

%package -n kernel-smp-pcmcia-net-hostap
Summary:	HostAP kernel drivers - PCMCIA SMP version
Summary(pl):	Sterowniki HostAP PCMCIA dla j±dra Linuksa SMP
Release:	%{rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%{?with_dist_kernel:%requires_releq_kernel_smp}
Requires(post,postun):	/sbin/depmod
Requires:	kernel(pcmcia)
Requires:	kernel-smp-net-hostap = %{version}-%{rel}@%{_kernel_ver_str}

%description -n kernel-smp-pcmcia-net-hostap
HostAP kernel drivers. SMP version.

%description -n kernel-smp-pcmcia-net-hostap -l pl
Sterowniki HostAP PCMCIA dla j±dra Linuksa SMP.

%package devel
Summary:        Header files for develop hostap driver based application
Summary(pl):    Pliki nag³ówkowe do bibliotek hostap-driver
Group:          Development/Libraries
# doesn't require kernel modules

%description devel
This package includes the header files necessary to develop
applications that use hostap.

%description devel -l pl
Ten pakiet zawiera pliki nag³ówkowe potrzebne do tworzenia aplikacji
u¿ywaj±cych sterownika hostap.

%prep
%setup -q -n hostap-driver-%{version}

%build
cd driver/modules
rm -rf built
mkdir -p built/{nondist,smp,up}
for cfg in %{?with_dist_kernel:%{?with_smp:smp} up}%{!?with_dist_kernel:nondist}; do
    if [ ! -r "%{_kernelsrcdir}/config-$cfg" ]; then
	exit 1
    fi
    rm -rf include
    install -d include/{linux,config}
    ln -sf %{_kernelsrcdir}/config-$cfg .config
    ln -sf %{_kernelsrcdir}/include/linux/autoconf-$cfg.h include/linux/autoconf.h
    ln -sf %{_kernelsrcdir}/include/asm-%{_target_base_arch} include/asm
    touch include/config/MARKER
    %{__make} -C %{_kernelsrcdir} clean \
        RCS_FIND_IGNORE="-name '*.ko' -o" \
        M=$PWD O=$PWD \
        %{?with_verbose:V=1}
    %{__make} -C %{_kernelsrcdir} modules \
        CC="%{__cc}" CPP="%{__cpp}" \
        M=$PWD O=$PWD \
        %{?with_verbose:V=1}
    mv *.ko built/$cfg
done

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}{,smp}/kernel/drivers/net/{pcmcia,wireless}
install -d $RPM_BUILD_ROOT%{_sysconfdir}/pcmcia
install -d $RPM_BUILD_ROOT%{_includedir}

install driver/etc/hostap_cs.conf \
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
%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/pcmcia/hostap_cs.conf
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
%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/pcmcia/hostap_cs.conf
/lib/modules/%{_kernel_ver}smp/kernel/drivers/net/pcmcia/*.ko*
%endif
%endif

%files devel
%defattr(644,root,root,755)
%{_includedir}/*.h
