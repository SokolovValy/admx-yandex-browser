%define _destdir %_datadir/PolicyDefinitions
%define _unpackaged_files_terminate_build 1

Name: admx-yandex-browser
Version: 104.0
Release: alt1

Summary: YandexBrowser-specific ADMX policy templates
License: CC-BY-2.5
Group: System/Configuration/Other
Url: https://yandex.ru/support/browser-corporate/deployment/deployment.html
BuildArch: noarch

BuildRequires: admx-lint
BuildRequires: iconv

Source0: policy_templates.tar

%description
YandexBrowser-specific ADMX files, which are registry-based policy settings
provide an XML-based structure for defining the display of the Administrative
Template policy settings in the Group Policy Object Editor.

%prep
%setup -q -n policy_templates

%install
mkdir -p %buildroot%_datadir
mkdir -p %buildroot%_destdir
cp -a ./* %buildroot%_destdir

%check
for file in %buildroot%_destdir/*.admx %buildroot%_destdir/*-*/*.adml; do
    admx-lint --input_file "$file"
done

%files
%dir %_destdir
%dir %_destdir/*-*/
%_destdir/*.admx
%_destdir/*/*.adml


%changelog
* Mon Oct 11 2022 Dmitriy Voropaev <voropaevdmtr@altlinux.org> 104.0-alt1
- Initial release
