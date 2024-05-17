# FIXME why does the dependency generator find all sorts of
# requirements that are in fact statically linked in?
%define __requires_exclude ocamlx?\\(.*
%define _disable_rebuild_configure 1

Name: coccinelle
Version: 1.2
Release: 1
Source0: https://github.com/coccinelle/coccinelle/archive/refs/tags/%{version}.tar.gz
Summary: Tool for source-to-source transformations of C code
URL: https://coccinelle.lip6.fr/
License: GPL-2.0
Group: Development/Tools
Patch1000: https://github.com/thierry-martinez/stdcompat/pull/33/commits/05337180c722fbb54fd51aa40db82555f1aef54f.patch
BuildRequires: autoconf
BuildRequires: automake
BuildRequires: ocaml
BuildRequires: pkgconfig(libpcre)
Provides: spatch = %{EVRD}

%description
Coccinelle allows programmers to easily write some complex
style-preserving source-to-source transformations on C source code,
like for instance to perform some refactorings.

%prep
%setup
%autopatch -M 999 -p1
cd bundles/stdcompat/stdcompat-current
%autopatch -m 1000 -p1
cd -
./autogen

%conf
# Out-of-tree builds currently fail
%configure

%build
%make_build opt-only

%install
%make_install

%if ! %{cross_compiling}
%check
LD_LIBRARY_PATH=$(pwd) ./spatch.opt -cocci_file demos/simple.cocci demos/simple.c
%endif

%files
%{_bindir}/spatch
%{_bindir}/spgen
%{_libdir}/coccinelle
%{_mandir}/man1/*.1*
%{_mandir}/man3/*.3*
%{_datadir}/bash-completion/completions/spatch
