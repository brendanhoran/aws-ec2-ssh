%{?systemd_requires}
%define name aws-ec2-ssh
%define version  1.2.0
%define archive  aws-ec2-ssh

Name: %{name}
Summary: Manage AWS EC2 SSH access with IAM
Version: %{version}
Release: 1

Group: System/Administration
License: MIT
URL: https://github.com/brendanhoran/aws-ec2-ssh
Source0: v%{version}.tar.gz
Source1: import_users
Source2: sshd_config
BuildArch: noarch
Packager: Brendan Horan
BuildRequires: systemd
Requires: bash, awscli


%description
Use your IAM user's public SSH key to get access via SSH to an EC2 instance.


%prep
%setup -q


%install
mkdir -p ${RPM_BUILD_ROOT}%{_bindir}
mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}/cron.d
install -m 700 import_users.sh ${RPM_BUILD_ROOT}%{_bindir}
install -m 700 authorized_keys_command.sh ${RPM_BUILD_ROOT}%{_bindir}
install -m 600 aws-ec2-ssh.conf ${RPM_BUILD_ROOT}%{_sysconfdir}/aws-ec2-ssh.conf
install -m 600 %{SOURCE1} ${RPM_BUILD_ROOT}%{_sysconfdir}/cron.d


%post
%systemd_postun_with_restart crond.service


%files
%defattr(-,root,root)
%attr(700,root,root) %{_bindir}/import_users.sh
%attr(700,root,root) %{_bindir}/authorized_keys_command.sh
%config %{_sysconfdir}/aws-ec2-ssh.conf
%config %{_sysconfdir}/cron.d/import_users


%changelog

* Wed Jun 20 2017 Brendan Horan <brendan@horan.hk>
- Refactor rpm spec and fork repo

* Wed May 3 2017 Michiel van Baak <michiel@vanbaak.eu> - 1.1.0-2
- Create cron.d file and run import_users on install

* Thu Apr 27 2017 Michiel van Baak <michiel@vanbaak.eu> - post-1.0-master
- use correct versioning based on fedora package versioning guide

* Sat Apr 15 2017 Michiel van Baak <michiel@vanbaak.eu> - pre-1.0
- Initial RPM spec file
