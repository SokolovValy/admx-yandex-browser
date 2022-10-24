%define _destdir %_datadir/PolicyDefinitions
%define _unpackaged_files_terminate_build 1

Name: admx-yandex-browser
Version: 104.0
Release: alt2

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
mkdir -p %buildroot%_destdir
cp -a ./* %buildroot%_destdir

[ -d %buildroot%_destdir/en-US ] ||
    cp -a %buildroot%_destdir/ru-RU %buildroot%_destdir/en-US

for file in %buildroot%_destdir/*.admx %buildroot%_destdir/*-*/*.adml; do
    if echo "$(basename "$file")" | grep -q "\.admx$"; then
        mv "$file" "$file.utf16"
        iconv -f UTF-16 -t UTF-8 <"$file.utf16" >"$file.cr"
        tr -d '\r' <"$file.cr" >"$file"
        rm -f "$file.utf16" "$file.cr"
    fi
    grep -q "^\(<policyDefinitions\|<policyDefinitionResources\) .*xmlns:xsd=" "$file" ||
        sed -i 's/\(<policyDefinitions\|<policyDefinitionResources\)/\1 xmlns:xsd="http:\/\/www.w3.org\/2001\/XMLSchema"/' "$file"
    grep -q "^\(<policyDefinitions\|<policyDefinitionResources\) .*xmlns:xsi=" "$file" ||
        sed -i 's/\(<policyDefinitions\|<policyDefinitionResources\)/\1 xmlns:xsi="http:\/\/www.w3.org\/2001\/XMLSchema-instance"/' "$file"
    grep -q "^\(<policyDefinitions\|<policyDefinitionResources\) .*xmlns=" "$file" ||
        sed -i 's/\(<policyDefinitions\|<policyDefinitionResources\)/\1 xmlns="http:\/\/schemas.microsoft.com\/GroupPolicy\/2006\/07\/PolicyDefinitions"/' "$file"
done

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
* Tue Oct 25 2022 Evgeny Sinelnikov <sin@altlinux.org> 104.0-alt2
- Update installation process for release 104.0.5112.114

* Tue Oct 11 2022 Dmitriy Voropaev <voropaevdmtr@altlinux.org> 104.0-alt1
- Initial release
