#
# Conditional build:
%bcond_without	wayland	# Wayland support
%bcond_without	x11	# X11 (Xlib/XCB) support

%define	api_version	1.2.198.0

Summary:	Vulkan API Tools
Summary(pl.UTF-8):	Narzędzia API Vulkan
Name:		Vulkan-Tools
Version:	%{api_version}
Release:	1
License:	Apache v2.0
Group:		Applications/Graphics
#Source0Download: https://github.com/KhronosGroup/Vulkan-Tools/tags
Source0:	https://github.com/KhronosGroup/Vulkan-Tools/archive/sdk-%{version}/%{name}-sdk-%{version}.tar.gz
# Source0-md5:	80b230159fb52aeb7fac1e83909ad57e
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
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description mock-icd
Dummy Vulkan ICD (driver).

%description mock-icd -l pl.UTF-8
Atrapa sterownika Vulkan.

%prep
%setup -qn %{name}-sdk-%{version}

%build
install -d build
cd build

%cmake .. \
	%{!?with_wayland:-DBUILD_WSI_WAYLAND_SUPPORT=OFF} \
	%{!?with_x11:-DBUILD_WSI_XCB_SUPPORT=OFF} \
	%{!?with_x11:-DBUILD_WSI_XLIB_SUPPORT=OFF} \
	-DGLSLANG_INSTALL_DIR=%{_prefix} \
	-DINSTALL_ICD=ON

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}/vulkan/icd.d

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%{__mv} $RPM_BUILD_ROOT%{_datadir}/vulkan/icd.d/VkICD_mock_icd.json \
	$RPM_BUILD_ROOT%{_sysconfdir}/vulkan/icd.d/VkICD_mock_icd.json.disabled

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc GOVERNANCE.md README.md vulkaninfo/vulkaninfo.md
%attr(755,root,root) %{_bindir}/vkcube
%attr(755,root,root) %{_bindir}/vkcubepp
%attr(755,root,root) %{_bindir}/vulkaninfo

%files mock-icd
%defattr(644,root,root,755)
%{_sysconfdir}/vulkan/icd.d/VkICD_mock_icd.json.disabled
%attr(755,root,root) %{_libdir}/libVkICD_mock_icd.so
