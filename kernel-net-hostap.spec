%define rel	0.3

%bcond_without dist_kernel	# don't use a packaged kernel
%bcond_without smp		# don't build the SMP modules

Summary:	HostAP kernel drivers
Summary(es):	Driveres del núcleo de HostAP
Summary(pl):	Sterowniki HostAP dla j±dra Linuksa
Name:		kernel-net-hostap
Version:	0.1.2
Release:	%{rel}@%{_kernel_ver_str}
License:	GPL
Group:		Base/Kernel
Source0:	http://hostap.epitest.fi/releases/hostap-driver-%{version}.tar.gz
# Source0-md5:	48dc3ddd8a8b1d47002b54f7a8fee7da
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
Buildroot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
HostAP kernel drivers.

%description -l es
Módulos de núcleo para HostAP.

%description -l pl
Sterowniki HostAP dla j±dra Linuksa.

%package -n kernel-smp-net-hostap
Summary:	HostAP kernel drivers - SMP version
Summary(es):	Driveres del núcleo de HostAP - versión SMP
Summary(pl):	Sterowniki HostAP dla j±dra Linuksa SMP
Release:	%{rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%if %{with dist_kernel}
%requires_releq_kernel_smp
Requires:	kernel(pcmcia)
%endif
Requires(post,postun):	/sbin/depmod

%description -n kernel-smp-net-hostap
HostAP kernel drivers. SMP version.

%description -n kernel-net-hostap -l es
Módulos de núcleo para HostAP. Versión SMP.

%description -n kernel-smp-net-hostap -l pl
Sterowniki HostAP dla j±dra Linuksa SMP.

%prep
%setup -q -n hostap-driver-%{version}
%patch0 -p1

%build
grep -v "SMP" %{_kernelsrcdir}/.config > kernel-config.up
cp kernel-config.up kernel-config.smp
echo "CONFIG_SMP=y" >> kernel-config.smp

ln -sf kernel-config.up kernel-config
mkdir -p kernel-up/lib/modules/%{_kernel_ver}
%{__make} pccard plx pci crypt hostap \
	install_pccard install_plx install_pci \
	CC="%{kgcc}" \
	KERNEL_PATH="%{_kernelsrcdir}" \
	KERNELRELEASE=%{_kernel_ver} \
	DESTDIR=$(pwd)/kernel-up

%if %{with smp}
ln -sf kernel-config.smp kernel-config
mkdir -p kernel-smp/lib/modules/%{_kernel_ver}smp
rm -f driver/modules/*.o	# UP modules
%{__make} pccard plx pci crypt hostap \
	install_pccard install_plx install_pci \
	CC="%{kgcc} -D__KERNEL_SMP=1" \
	KERNEL_PATH="%{_kernelsrcdir}" \
	KERNELRELEASE=%{_kernel_ver}smp \
	DESTDIR=$(pwd)/kernel-smp
%endif

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}{,smp}

#kernel drivers
cp -a kernel-up/lib/modules/%{_kernel_ver}/* $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}
%if %{with smp}
cp -a kernel-smp/lib/modules/%{_kernel_ver}smp/* $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp
%endif

%post
%depmod %{_kernel_ver}

%preun
%depmod %{_kernel_ver}

%post -n kernel-smp-net-hostap
%depmod %{_kernel_ver}smp

%postun -n kernel-smp-net-hostap
%depmod %{_kernel_ver}smp

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/net/*.o*
/lib/modules/%{_kernel_ver}/pcmcia/*.o*

%if %{with smp}
%files -n kernel-smp-net-hostap
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}smp/net/*.o*
/lib/modules/%{_kernel_ver}smp/pcmcia/*.o*
%endif
