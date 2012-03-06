#Module-Specific definitions
%define apache_version 2.4.0
%define mod_name mod_auth_radius
%define load_order 114

Summary:	DSO module for the apache Web server
Name:		apache-%{mod_name}
Version:	1.5.8
Release:	9
Group:		System/Servers
License:	Apache License
URL:		http://www.freeradius.org/mod_auth_radius/
Source0:	ftp://ftp.freeradius.org/pub/radius/mod_auth_radius-%{version}.tar.gz
Patch0:		mod_auth_radius-1.5.8-CAN2005-0108.diff
Patch1:		mod_auth_radius-1.5.8-apache241.diff
Requires(pre): rpm-helper
Requires(postun): rpm-helper
Requires:	apache >= %{apache_version}
BuildRequires:  apache-devel >= %{apache_version}
Epoch:		2

%description
Make apache a RADIUS client for authentication and accounting requests.

%prep

%setup -q -n mod_auth_radius-%{version}
%patch0 -p0
%patch1 -p0

cp mod_auth_radius-2.0.c mod_auth_radius.c

%build
apxs -c mod_auth_radius.c -Wl,-lresolv

%install

install -d %{buildroot}%{_libdir}/apache
install -d %{buildroot}%{_sysconfdir}/httpd/modules.d

install -m0755 .libs/*.so %{buildroot}%{_libdir}/apache/

cat > %{buildroot}%{_sysconfdir}/httpd/modules.d/%{load_order}_%{mod_name}.conf << EOF
LoadModule radius_auth_module %{_libdir}/apache/%{mod_name}.so
EOF

%post
/bin/systemctl daemon-reload >/dev/null 2>&1 || :

%postun
if [ "$1" = "0" ]; then
    /bin/systemctl daemon-reload >/dev/null 2>&1 || :
fi

%files
%doc README htaccess httpd.conf index.html
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/*.conf
%attr(0755,root,root) %{_libdir}/apache/*.so
