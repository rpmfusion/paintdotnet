Name:           paintdotnet
Version:        0.1.63
Release:        6%{?dist}
Summary:        A mono port of the Paint.NET image editor

# Mono is unavailable on ppc64 prior to Fedora 11
%if 0%{?fedora} < 11
ExcludeArch:    ppc64
%endif

Group:          Applications/Multimedia
License:        MIT and CC-BY-NC-ND
# The software is licensed as per MIT License with 3 exceptions:
# 1. The Paint.NET logo and icon artwork are Copyright Rich Brewster
# They are covered by the CC-BY-NC-ND license
# 2. Certain text and graphic resources (e.g., toolbar icon graphics,
# text for menu items and the status bar). These are collectively referred
# to as "resource assets" and are defined to include the contents of files
# installed by Paint.NET, or included in its source code distribution, that
# have a .RESOURCES, .RESX, or .PNG file extension. This also includes embedded
# resource files within the PaintDotNet.Resources.dll installed file. These
# "resource assets" are covered by the Creative Commons
# Attribution-NonCommercial-NoDerivs 2.5 license.
# 3. Although the Paint.NET source code distribution includes the GPC source
# code, use of the GPC code in any other commercial application is not
# permitted without a GPC Commercial Use Licence from The University of
# Manchester. For more information, please refer to the GPC website at: 
# http://www.cs.man.ac.uk/~toby/alan/software/
# Exception 3 above does not apply here as the GPC library is not part of
# paintdotnet 3.0, packaged here
URL:            http://paint-mono.googlecode.com/
Source0:        http://paint-mono.googlecode.com/files/%{name}-%{version}.tar.gz
Source2:        paintdotnet.desktop
# http://code.google.com/p/paint-mono/issues/detail?id=20
Patch0:         paintdotnet-x64.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  mono-core desktop-file-utils ImageMagick
Requires:       hicolor-icon-theme

# disabling empty mono debuginfo package
%global debug_package %{nil}

%description
Paint.NET is an image and photo editing software. It features an intuitive
and innovative user interface with support for layers, unlimited undo, special
effects, and a wide variety of useful and powerful tools. An active and growing
online community provides friendly help, tutorials, and plugins.

%package devel
Summary:        Pkgconfig files for paintdotnet
Group:          Development/Libraries
Requires:       pkgconfig paintdotnet = %{version}-%{release}

%description devel
pkgconfig files for paintdotnet

%prep
%setup -q
%patch0 -p1 -b .x64

convert Resources/Icons/PaintDotNet.ico Resources/Icons/PaintDotNet.png

%build
./configure --prefix=%{_prefix} --libdir=%{_libdir}

make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

install -D ./Resources/Icons/PaintDotNet-4.png \
  ${RPM_BUILD_ROOT}%{_datadir}/icons/hicolor/256x256/apps/paintdotnet.png
install -D ./Resources/Icons/PaintDotNet-5.png \
  ${RPM_BUILD_ROOT}%{_datadir}/icons/hicolor/48x48/apps/paintdotnet.png
install -D ./Resources/Icons/PaintDotNet-6.png \
  ${RPM_BUILD_ROOT}%{_datadir}/icons/hicolor/32x32/apps/paintdotnet.png
install -D ./Resources/Icons/PaintDotNet-7.png \
  ${RPM_BUILD_ROOT}%{_datadir}/icons/hicolor/16x16/apps/paintdotnet.png

# Moving *.pc files from devel package to _libdir/pkgconfig/paintdotnet/
# Would be better if pc files where named in a less generic way
# Should addressed by upstream
mkdir -p ${RPM_BUILD_ROOT}%{_libdir}/pkgconfig/paintdotnet
mv ${RPM_BUILD_ROOT}%{_libdir}/pkgconfig/*.pc ${RPM_BUILD_ROOT}%{_libdir}/pkgconfig/paintdotnet/

desktop-file-install                             \
 --vendor=""                                     \
 --add-category X-Red-Hat-Extra                  \
 --dir=${RPM_BUILD_ROOT}%{_datadir}/applications \
 %{SOURCE2}

%clean
rm -rf $RPM_BUILD_ROOT

%post
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%files
%defattr(-,root,root,-)
%doc Resources/Files/License.txt Resources/Files/AboutCredits.rtf
%{_bindir}/*
%{_libdir}/paintdotnet/
%{_datadir}/applications/paintdotnet.desktop
%{_datadir}/icons/hicolor/256x256/apps/paintdotnet.png
%{_datadir}/icons/hicolor/48x48/apps/paintdotnet.png
%{_datadir}/icons/hicolor/32x32/apps/paintdotnet.png
%{_datadir}/icons/hicolor/16x16/apps/paintdotnet.png

%files devel
%defattr(-,root,root,-)
%{_libdir}/pkgconfig/paintdotnet/

%changelog
* Thu Feb 09 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.1.63-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Jun 17 2009 - Eric Moret <eric.moret@gmail.com> - 0.1.63-5
- _libdir/pkgconfig/paintdotnet/ now owned by paintdotnet

* Mon Jun 15 2009 - Eric Moret <eric.moret@gmail.com> - 0.1.63-4
- Moving pc files from the devel package to _libdir/pkgconfig/paintdotnet/

* Wed Jun 3 2009 - Eric Moret <eric.moret@gmail.com> - 0.1.63-3
- Converting the ico file to png at build time

* Tue May 26 2009 - Eric Moret <eric.moret@gmail.com> - 0.1.63-2
- Fixing spec based on package review comments

* Tue Apr 28 2009 - Eric Moret <eric.moret@gmail.com> - 0.1.63-1
- update x64 build patch to upstream 0.1.63
- adding --vendor=""

* Fri Apr 17 2009 - Eric Moret <eric.moret@gmail.com> - 0.1.63-0.6
- Updating to use official source tarball
- adding icon extraction script

* Wed Feb 25 2009 - Eric Moret <eric.moret@gmail.com> - 0.1-0.5.63svn
- Updating desktop file for proper building on CentOS5

* Tue Feb 24 2009 - Eric Moret <eric.moret@gmail.com> - 0.1-0.4.63svn
- Removing Microsoft.Ink and Interop.Wia from the source tarball

* Mon Feb 23 2009 - Eric Moret <eric.moret@gmail.com> - 0.1-0.3.63svn
- Adding patch to remove Microsoft.Ink.dll and Interop.WIA.dll prior to building

* Fri Feb 20 2009 - Eric Moret <eric.moret@gmail.com> - 0.1-0.2.63svn
- Adding icon cache updates
- Adding instructions to generate tarball
- Changing license from CC-BY-ND to CC-BY-NC-ND for the Paint.NET logo

* Thu Feb 12 2009 - Eric Moret <eric.moret@gmail.com> - 0.1-0.1.63svn
- Initial spec
