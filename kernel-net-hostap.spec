%define rel	0.1

%define		no_install_post_compress_modules	1

%bcond_without dist_kernel	# don't use a packaged kernel
%bcond_without smp		# don't build the SMP modules

Summary:	HostAP kernel drivers
Summary(es):	Driveres del núcleo de HostAP
Summary(pl):	Sterowniki HostAP dla j±dra Linuksa
Name:		kernel-net-hostap
Version:	0.2.2
Release:	%{rel}@%{_kernel_ver_str}
License:	GPL
Group:		Base/Kernel
Source0:	http://hostap.epitest.fi/releases/hostap-driver-%{version}.tar.gz
Patch0:		hostap-driver-complex.patch
URL:		http://hostap.epitest.fi/
BuildRequires:	%{kgcc_package}
BuildRequires:	rpmbuild(macros) >= 1.118
%if %{with dist_kernel}
BuildRequires:	kernel-headers
%requires_releq_kernel_up
%endif
Requires:	kernel(pcmcia)
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
Requires:	kernel(pcmcia)
Group:		Base/Kernel
Requires(post,postun):	/sbin/depmod

%description -n kernel-pcmcia-net-hostap
HostAP PCMCIA kernel drivers.

%description -l pl -n kernel-pcmcia-net-hostap
Sterowniki HostAP PCMCIA dla j±dra Linuksa.

%package -n kernel-smp-net-hostap
Summary:	HostAP kernel drivers - SMP version
Summary(es):	Driveres del núcleo de HostAP - versión SMP
Summary(pl):	Sterowniki HostAP dla j±dra Linuksa SMP
Release:	%{rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%if %{with dist_kernel}
%requires_releq_kernel_smp
%endif
Requires(post,postun):	/sbin/depmod

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
Requires:	kernel(pcmcia)
Requires(post,postun):	/sbin/depmod

%description -n kernel-smp-pcmcia-net-hostap
HostAP kernel drivers. SMP version.

%description -n kernel-smp-pcmcia-net-hostap -l pl
Sterowniki HostAP PCMCIA dla j±dra Linuksa SMP.

%prep
%setup -q -n hostap-driver-%{version}
%patch0 -p0

%build
rm -rf build-done
install -d build-done/{UP,SMP}
cd driver/modules
ln -sf %{_kernelsrcdir}/config-up .config
rm -rf include
install -d include/{linux,config}
ln -s %{_kernelsrcdir}/include/linux/autoconf.h include/linux/autoconf.h
ln -s %{_kernelsrcdir}/include/asm-i386 include/asm
touch include/config/MARKER

%{__make} -C %{_kernelsrcdir} SUBDIRS=$PWD O=$PWD V=1 modules
mv *.ko ../../build-done/UP/

#%{__make} -C %{_kernelsrcdir} SUBDIRS=$PWD O=$PWD V=1 mrproper

ln -sf %{_kernelsrcdir}/config-up .config
rm -rf include
install -d include/{linux,config}
ln -s %{_kernelsrcdir}/include/linux/autoconf.h include/linux/autoconf.h
ln -s %{_kernelsrcdir}/include/asm-i386 include/asm
touch include/config/MARKER

%{__make} -C %{_kernelsrcdir} SUBDIRS=$PWD O=$PWD V=1 modules
mv *.ko ../../build-done/SMP/

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}{,smp}/kernel/drivers/{net,pcmcia}

#kernel drivers
cp -a build-done/UP/hostap.* $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/kernel/drivers/net/
cp -a build-done/UP/hostap_crypt* $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/kernel/drivers/net/
cp -a build-done/UP/hostap_plx.* $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/kernel/drivers/net/

cp -a build-done/UP/hostap_cs* $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/kernel/drivers/pcmcia/
cp -a build-done/UP/hostap_pci* $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/kernel/drivers/pcmcia/

%if %{with smp}
cp -a build-done/SMP/hostap.* $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp/kernel/drivers/net/
cp -a build-done/SMP/hostap_crypt* $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp/kernel/drivers/net/
cp -a build-done/SMP/hostap_plx.* $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp/kernel/drivers/net/

cp -a build-done/SMP/hostap_cs** $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp/kernel/drivers/pcmcia/
cp -a build-done/SMP/hostap_pci* $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp/kernel/drivers/pcmcia/
%endif

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
/lib/modules/%{_kernel_ver}/kernel/drivers/net/*.ko

%files -n kernel-pcmcia-net-hostap
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/kernel/drivers/pcmcia/*.ko

%files -n kernel-smp-net-hostap
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}smp/kernel/drivers/net/*.ko

%files -n kernel-smp-pcmcia-net-hostap
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}smp/kernel/drivers/pcmcia/*.ko
