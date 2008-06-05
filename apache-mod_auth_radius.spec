#Module-Specific definitions
%define apache_version 2.2.4
%define mod_name mod_auth_radius
%define mod_conf 14_%{mod_name}.conf
%define mod_so %{mod_name}.so

Summary:	DSO module for the apache Web server
Name:		apache-%{mod_name}
Version:	1.5.7
Release:	%mkrel 14
Group:		System/Servers
License:	Apache License
URL:		http://www.freeradius.org/mod_auth_radius/
Source0:	ftp://ftp.freeradius.org/pub/radius/mod_auth_radius.tar.bz2
Source1:	%{mod_conf}
Patch0:		mod_auth_radius-1.5.7-CAN2005-0108.diff
Patch1:		mod_auth_radius-2.0.c.diff
Patch2:		mod_auth_radius-1.5.7-apr1.diff
Requires(pre): rpm-helper
Requires(postun): rpm-helper
Requires(pre):  apache-conf >= %{apache_version}
Requires(pre):  apache >= %{apache_version}
Requires:	apache-conf >= %{apache_version}
Requires:	apache >= %{apache_version}
BuildRequires:  apache-devel >= %{apache_version}
Epoch:		2
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
Make apache a RADIUS client for authentication and accounting requests.

%prep

%setup -q -n mod_auth_radius-%{version}
%patch0 -p0
%patch1 -p0
%patch2 -p0

cp mod_auth_radius-2.0.c mod_auth_radius.c
cp %{SOURCE1} %{mod_conf}

%build
%{_sbindir}/apxs -c mod_auth_radius.c -Wl,-lresolv

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

install -d %{buildroot}%{_libdir}/apache-extramodules
install -d %{buildroot}%{_sysconfdir}/httpd/modules.d

install -m0755 .libs/*.so %{buildroot}%{_libdir}/apache-extramodules/
install -m0644 %{mod_conf} %{buildroot}%{_sysconfdir}/httpd/modules.d/%{mod_conf}

%post
if [ -f %{_var}/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart 1>&2;
fi

%postun
if [ "$1" = "0" ]; then
    if [ -f %{_var}/lock/subsys/httpd ]; then
        %{_initrddir}/httpd restart 1>&2
    fi
fi

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc README htaccess httpd.conf index.html
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/%{mod_conf}
%attr(0755,root,root) %{_libdir}/apache-extramodules/%{mod_so}
