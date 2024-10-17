#Module-Specific definitions
%define apache_version 2.2.4
%define mod_name mod_auth_radius
%define mod_conf 14_%{mod_name}.conf
%define mod_so %{mod_name}.so

Summary:	DSO module for the apache Web server
Name:		apache-%{mod_name}
Version:	1.5.8
Release:	20
Group:		System/Servers
License:	Apache License
URL:		https://www.freeradius.org/mod_auth_radius/
Source0:	ftp://ftp.freeradius.org/pub/radius/mod_auth_radius-%{version}.tar.gz
Source1:	%{mod_conf}
Patch0:		mod_auth_radius-1.5.8-CAN2005-0108.diff
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

cp mod_auth_radius-2.0.c mod_auth_radius.c
cp %{SOURCE1} %{mod_conf}

%build
%{_bindir}/apxs -c mod_auth_radius.c -Wl,-lresolv

%install
rm -rf %{buildroot}

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
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc README htaccess httpd.conf index.html
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/%{mod_conf}
%attr(0755,root,root) %{_libdir}/apache-extramodules/%{mod_so}


%changelog
* Sat May 14 2011 Oden Eriksson <oeriksson@mandriva.com> 2:1.5.8-7mdv2011.0
+ Revision: 674422
- rebuild

* Mon May 02 2011 Oden Eriksson <oeriksson@mandriva.com> 2:1.5.8-6
+ Revision: 662770
- mass rebuild

* Sun Oct 24 2010 Oden Eriksson <oeriksson@mandriva.com> 2:1.5.8-5mdv2011.0
+ Revision: 588276
- rebuild

* Mon Mar 08 2010 Oden Eriksson <oeriksson@mandriva.com> 2:1.5.8-4mdv2010.1
+ Revision: 515831
- rebuilt for apache-2.2.15

* Wed Sep 30 2009 Oden Eriksson <oeriksson@mandriva.com> 2:1.5.8-3mdv2010.0
+ Revision: 451695
- rebuild

* Fri Jul 31 2009 Oden Eriksson <oeriksson@mandriva.com> 2:1.5.8-2mdv2010.0
+ Revision: 405123
- rebuild

* Sun Jun 21 2009 Oden Eriksson <oeriksson@mandriva.com> 2:1.5.8-1mdv2010.0
+ Revision: 387642
- 1.5.8
- rediffed P0 (CAN2005-0108)
- dropped redundant patches

* Wed Jan 07 2009 Oden Eriksson <oeriksson@mandriva.com> 2:1.5.7-16mdv2009.1
+ Revision: 326479
- rebuild

* Mon Jul 14 2008 Oden Eriksson <oeriksson@mandriva.com> 2:1.5.7-15mdv2009.0
+ Revision: 235636
- rebuild

* Thu Jun 05 2008 Oden Eriksson <oeriksson@mandriva.com> 2:1.5.7-14mdv2009.0
+ Revision: 215286
- rebuild

* Fri Mar 07 2008 Oden Eriksson <oeriksson@mandriva.com> 2:1.5.7-13mdv2008.1
+ Revision: 181435
- rebuild

* Mon Feb 18 2008 Thierry Vignaud <tv@mandriva.org> 2:1.5.7-12mdv2008.1
+ Revision: 170708
- rebuild
- fix "foobar is blabla" summary (=> "blabla") so that it looks nice in rpmdrake

* Fri Jan 11 2008 Thierry Vignaud <tv@mandriva.org> 2:1.5.7-11mdv2008.1
+ Revision: 148462
- rebuild
- kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Sat Sep 08 2007 Oden Eriksson <oeriksson@mandriva.com> 2:1.5.7-10mdv2008.0
+ Revision: 82356
- rebuild

* Thu Aug 16 2007 Oden Eriksson <oeriksson@mandriva.com> 2:1.5.7-9mdv2008.0
+ Revision: 64316
- use the new %%serverbuild macro

* Wed Jun 13 2007 Oden Eriksson <oeriksson@mandriva.com> 2:1.5.7-8mdv2008.0
+ Revision: 38408
- rebuild


* Sat Mar 10 2007 Oden Eriksson <oeriksson@mandriva.com> 1.5.7-7mdv2007.1
+ Revision: 140578
- rebuild

* Tue Feb 27 2007 Oden Eriksson <oeriksson@mandriva.com> 2:1.5.7-6mdv2007.1
+ Revision: 126606
- general cleanups

* Thu Nov 09 2006 Oden Eriksson <oeriksson@mandriva.com> 2:1.5.7-5mdv2007.0
+ Revision: 79231
- Import apache-mod_auth_radius

* Sun Jul 30 2006 Oden Eriksson <oeriksson@mandriva.com> 2:1.5.7-5mdv2007.0
- rebuild

* Mon Dec 12 2005 Oden Eriksson <oeriksson@mandriva.com> 1.5.7-4mdk
- rebuilt against apache-2.2.0

* Sun Oct 30 2005 Oden Eriksson <oeriksson@mandriva.com> 1.5.7-3mdk
- rebuilt to provide a -debug package too

* Mon Oct 17 2005 Oden Eriksson <oeriksson@mandriva.com> 2:1.5.7-2mdk
- rebuilt against correct apr-0.9.7

* Sat Oct 15 2005 Oden Eriksson <oeriksson@mandriva.com> 2:1.5.7-1mdk
- rebuilt for apache-2.0.55

* Sat Jul 30 2005 Oden Eriksson <oeriksson@mandriva.com> 2.0.54_1.5.7-4mdk
- added another work around for a rpm bug

* Sat Jul 30 2005 Oden Eriksson <oeriksson@mandriva.com> 2.0.54_1.5.7-3mdk
- added a work around for a rpm bug, "Requires(foo,bar)" don't work

* Tue Jun 07 2005 Oden Eriksson <oeriksson@mandriva.com> 1:2.0.54_1.5.7-2mdk
- use epoch 1

* Tue Jun 07 2005 Oden Eriksson <oeriksson@mandriva.com> 2.0.54_1.5.7-1mdk
- use the code from freeradius.org instead as the previous one 
  won't compile with gcc4
- dropped the old patches and added one new one from cvs and a
  fix for CAN2005-0108 by debian.
- new config file (14_mod_auth_radius.conf)

* Fri May 27 2005 Oden Eriksson <oeriksson@mandriva.com> 2.0.54_1.7PR1-1mdk
- rename the package
- the conf.d directory is renamed to modules.d
- use new rpm-4.4.x pre,post magic

* Thu Mar 17 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.53_1.7PR1-6mdk
- use the %%mkrel macro

* Sun Feb 27 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.53_1.7PR1-5mdk
- fix %%post and %%postun to prevent double restarts

* Wed Feb 16 2005 Stefan van der Eijk <stefan@eijk.nu> 2.0.53_1.7PR1-4mdk
- fix bug #6574

* Wed Feb 16 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.53_1.7PR1-3mdk
- fix deps

* Tue Feb 15 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.53_1.7PR1-2mdk
- spec file cleanups, remove the ADVX-build stuff

* Tue Feb 08 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.53_1.7PR1-1mdk
- rebuilt for apache 2.0.53

* Wed Sep 29 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.52_1.7PR1-1mdk
- built for apache 2.0.52

* Fri Sep 17 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.51_1.7PR1-1mdk
- built for apache 2.0.51

* Wed Aug 11 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.50_1.7PR1-3mdk
- rebuilt

* Tue Jul 13 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.50_1.7PR1-2mdk
- remove redundant provides

* Thu Jul 01 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.50_1.7PR1-1mdk
- built for apache 2.0.50

* Sat Jun 12 2004 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.49_1.7PR1-1mdk
- built for apache 2.0.49

