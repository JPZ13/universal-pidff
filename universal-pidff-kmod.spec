Name:           universal-pidff-kmod
Version:        0.0.10
Release:        1%{?dist}
Summary:        Universal FFB Driver for Moza/Cammus/VRS and more
License:        GPLv2
URL:            https://github.com/JacKeTUs/universal-pidff
Source0:        https://github.com/JacKeTUs/universal-pidff/archive/refs/tags/%{version}.tar.gz

# get the proper build-sysbuild package from the repo, which
# tracks in all the kernel-devel packages
BuildRequires:  %{_bindir}/kmodtool
BuildRequires:  make

%define buildforkernels akmod

%global debug_package %{nil}

%{expand:%(kmodtool --target %{_target_cpu} --repo rpmfusion --kmodname %{name} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null) }

%description
Universal Force Feedback (FFB) Driver for Moza, Cammus, VRS, and other devices. Kmod version.

%prep
%setup -n %{name}-%{version}
%{?kmodtool_check}
kmodtool  --target %{_target_cpu}  --repo %{repo} --kmodname %{name} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null

for kernel_version in %{?kernel_versions} ; do
    cp -a %{name} _kmod_build_${kernel_version%%___*}
done

%build
for kernel_version in %{?kernel_versions}; do
    make %{?_smp_mflags} -C "${kernel_version##*___}" M=${PWD}/_kmod_build_${kernel_version%%___*} modules
done

%install
rm -rf %{buildroot}
for kernel_version in %{?kernel_versions}; do
    mkdir -p %{buildroot}/%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}
    install -D -m 755 _kmod_build_${kernel_version%%___*}/*.ko %{buildroot}/%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/
done
%{?akmod_install}

%clean
rm -rf %{buildroot}

%changelog
%autochangelog
