%define opt %(test -x %{_bindir}/ocamlopt && echo 1 || echo 0)
%define debug_package %{nil}
%define name coccinelle
%define versionbase 1.0.0
%define releasecandidate rc7
%define release 2
%define versioncomplete %{versionbase}-%{releasecandidate}

%if !%opt
# Prevent RPM from stripping bytecode /usr/bin/spatch.
%define __strip /bin/true
%endif

Name:           %{name}
Version:        %{versionbase}.%{releasecandidate}
Release:        %{release}
Summary:        Semantic patching for Linux (spatch)
Group:          Development/C
License:        GPLv2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-buildroot
URL:            http://coccinelle.lip6.fr/
Source0:        http://coccinelle.lip6.fr/distrib/%{name}-%{versioncomplete}.tgz
BuildRequires:  ocaml >= 3.10.0
BuildRequires:  ocaml-findlib-devel
BuildRequires:  ocaml-doc
BUildRequires:	ncurses-devel
BuildRequires:  python-devel
%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
BuildRequires:  chrpath

%global __ocaml_requires_opts -i Ast_c -i Token_c -i Type_cocci -i Ast_cocci -i Common -i Oassocb -i ANSITerminal -i Oseti -i Sexplib -i Oassoch -i Setb -i Oassoc_buffer -i Ograph2way -i SetPt -i Mapb -i Dumper -i Osetb -i Flag


%description
Coccinelle is a tool to utilize semantic patches for manipulating C
code. It was originally designed to ease maintenance of device
drivers in the Linux kernel.


%package doc
Summary:        Documentation for %{name}
Group:          Development/C
Requires:       %{name} = %{version}-%{release}


%description doc
The %{name}-doc package contains documentation for %{name}.


%package examples
Summary:        Examples for %{name}
Group:          Development/C
Requires:       %{name} = %{version}-%{release}


%description examples
The %{name}-examples package contains examples for %{name}.


%prep
%setup -q -n %{name}-%{versioncomplete}

# Remove .cvsignore files.
find -name .cvsignore -delete

# Convert a few files to UTF-8 encoding.
for f in demos/demo_rule9/sym53c8xx.res demos/demo_rule9/sym53c8xx.c; do
  mv $f $f.orig
  iconv -f iso-8859-1 -t utf-8 < $f.orig > $f
  rm $f.orig
done


%build
./configure --prefix=%{_prefix}
%{__sed} -i \
  -e 's,LIBDIR=.*,LIBDIR=%{_libdir},' \
  -e 's,MANDIR=.*,MANDIR=%{_mandir},' \
  -e 's,SHAREDIR=.*,SHAREDIR=%{_datadir}/%{name},' \
  Makefile.config

# Note that _smp_mflags breaks the build.
%if !%opt
make all
%else
make all opt
%endif


%install
rm -rf $RPM_BUILD_ROOT
%make DESTDIR=$RPM_BUILD_ROOT install

%if %opt
# Just the native code version.
rm $RPM_BUILD_ROOT%{_bindir}/spatch
mv $RPM_BUILD_ROOT%{_bindir}/spatch.opt $RPM_BUILD_ROOT%{_bindir}/spatch
strip $RPM_BUILD_ROOT%{_datadir}/%{name}/spatch.opt
%else
# Else prevent prelink from buggering about with the bytecode binary.
mkdir -p $RPM_BUILD_ROOT/etc/prelink.conf.d
echo '-b %{_bindir}/spatch' \
  > $RPM_BUILD_ROOT/etc/prelink.conf.d/%{name}.conf
%endif

strip $RPM_BUILD_ROOT%{_libdir}/*.so
chrpath --delete $RPM_BUILD_ROOT%{_libdir}/*.so

# Remove bogus Makefiles from Python directory.
find $RPM_BUILD_ROOT%{_datadir}/%{name} -name Makefile -delete

# Move Python libraries to python lib directory.
mkdir -p $RPM_BUILD_ROOT%{python_sitelib}
mv $RPM_BUILD_ROOT%{_datadir}/%{name}/python/coccilib \
  $RPM_BUILD_ROOT%{python_sitelib}

rmdir $RPM_BUILD_ROOT%{_datadir}/%{name}/python


%check
LD_LIBRARY_PATH=. \
./spatch.opt -cocci_file demos/simple.cocci demos/simple.c


%files
%doc authors.txt bugs.txt changes.txt copyright.txt
%doc credits.txt install.txt license.txt readme.txt
%{_bindir}/spatch
%{_datadir}/%{name}/
%{python_sitelib}/coccilib/
%{_mandir}/man1/*.1*
%{_mandir}/man3/*.3*
%{_libdir}/*.so
%if !%opt
%config(noreplace) /etc/prelink.conf.d/%{name}.conf
%endif


%files doc
%doc docs


%files examples
%doc demos


%changelog
* Mon Sep 19 2011 Alexandre Lissy <alissy@mandriva.com> 1.0.0.rc7-1
+ Revision: 700362
- Updating to 1.0.0-rc7
  Removing %%make in favor of make

* Fri Aug 12 2011 Alexandre Lissy <alissy@mandriva.com> 1.0.0.rc5-1
+ Revision: 694208
- Updating coccinelle to latest 1.0.0-rc5 release

* Mon Aug 01 2011 Alexandre Lissy <alissy@mandriva.com> 1.0.0.rc4-1
+ Revision: 692680
- Update sources with rc4
- .spec cleanup
- Use %%make macro
- Updating to rc4

* Fri Jun 24 2011 Alexandre Lissy <alissy@mandriva.com> 1.0.0.rc3-1
+ Revision: 686882
- Missing man page
- Updating coccinelle to 1.0.0 rc3

* Mon May 30 2011 Alexandre Lissy <alissy@mandriva.com> 1.0.0.rc2-1
+ Revision: 681850
- fix: Setting Group to Development/C for all packages built
- fix: Adding missing BuildRequires on ncurses-devel
- Changing group to Development/C
- Introducing coccinelle, a program matching and tranformation for C source code.
  Package imported from Fedora.
  Some adjustments to Mandriva.
  Updating Coccinelle to 1.0.0-rc2
- Created package structure for coccinelle.

