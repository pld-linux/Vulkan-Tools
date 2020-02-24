
# Conditional build:
%bcond_with	tests	# run tests

%define	api_version	1.2.133

Summary:	Vulkan API Tools
Summary(pl.UTF-8):	Narzędzia API Vulkan
Name:		Vulkan-Tools
Version:	%{api_version}
Release:	1
License:	Apache v2.0
Group:		Development
Source0:	https://github.com/KhronosGroup/Vulkan-Tools/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	f64b1064d114ff0ca5f140781a0973b1
URL:		https://github.com/KhronosGroup/Vulkan-Tools/
BuildRequires:	Vulkan-Loader-devel >= %{api_version}
BuildRequires:	cmake >= 3.10.2
BuildRequires:	glslang
%{?with_x11:BuildRequires:	libxcb-devel}
BuildRequires:	pkgconfig
BuildRequires:	python3 >= 1:3
BuildRequires:	python3-lxml
BuildRequires:	python3-modules >= 1:3
%{?with_wayland:BuildRequires:	wayland-devel}
%{?with_x11:BuildRequires:	xorg-lib-libX11-devel}
Obsoletes:	vulkan-sdk-demos
Obsoletes:	vulkan-sdk-tools
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Tools for the Vulkan graphics API.

%description -l pl.UTF-8
Narzędzia do graficznego API Vulkan.

%package mock-icd
Summary:	Dummy Vulkan ICD (driver)
Summary(pl.UTF-8):	Atrapa sterownika Vulkan
Group:		Development
Requires:	%{name} = %{version}-%{release}

%description mock-icd
Dummy Vulkan ICD (driver).

%description mock-icd -l pl.UTF-8
Atrapa sterownika Vulkan.

%prep
%setup -qn %{name}-%{version}

%build
install -d build
cd build

# .pc file creation expect CMAKE_INSTALL_LIBDIR to be relative (to CMAKE_INSTALL_PREFIX)
%cmake .. \
	-DCMAKE_INSTALL_LIBDIR=%{_lib} \
	-DGLSLANG_INSTALL_DIR=%{_prefix} \
	-DBUILD_TESTS=%{?with_tests:ON}%{!?with_tests:OFF} \
	-DINSTALL_ICD=ON

%{__make}

%if %{with tests}
cd tests
LC_ALL=C.UTF-8 VK_LAYER_PATH=layers LD_LIBRARY_PATH=../loader:layers ./run_loader_tests.sh
cd ..
%endif

cd ..

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_sysconfdir}/vulkan/icd.d/

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

mv $RPM_BUILD_ROOT%{_datadir}/vulkan/icd.d/VkICD_mock_icd.json \
	$RPM_BUILD_ROOT%{_sysconfdir}/vulkan/icd.d/VkICD_mock_icd.json.disabled

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.md GOVERNANCE.md CONTRIBUTING.md
%attr(755,root,root) %{_bindir}/vkcube
%attr(755,root,root) %{_bindir}/vkcubepp
%attr(755,root,root) %{_bindir}/vulkaninfo

%files mock-icd
%defattr(644,root,root,755)
%{_sysconfdir}/vulkan/icd.d/VkICD_mock_icd.json.disabled
%attr(755,root,root) %{_libdir}/libVkICD_mock_icd.so
