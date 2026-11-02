# Judge file r2-terraform-1.16.7

## PUBLISHED RELEASE NOTES (written by the maintainers)

## 1.16.7 (October 22, 2026)


BUG FIXES:

* command/test: Avoid panic when testing schema w/ deprecated values ([#39406](https://github.com/hashicorp/terraform/issues/39406))


NOTES:

* Terraform is now built with Go 1.26.10, which no longer trusts certificates issued through a set of compromised eMudhra intermediate CAs (CVE-2026-111943) ([#39417](https://github.com/hashicorp/terraform/issues/39417))




## COMMIT SUBJECTS between the previous tag and the release

Cleanup after 1.16.6 release (#39388)
Backport of command/test: Avoid panic when testing schema w/ deprecated values into v1.16 (#39410)
backport of commit 0177d6916e1e88cf01cedc342f2a1a9ca4ab6f13
backport of commit 8ea3b5303387bca7a2d6b1b9bc284f3113c5efb2
Prepare before 1.16.7 release

# CANDIDATE A

## 1.16.7 (October 22, 2026)

BUG FIXES:

* `terraform test`: Fixed a crash when a failed assertion involved a value from a deprecated schema attribute. ([#39410](https://github.com/hashicorp/terraform/pull/39410))

NOTES:

* Terraform is now built with Go 1.26.10 (previously 1.26.8). Per the project changelog, this Go version no longer trusts certificates issued through a set of compromised eMudhra intermediate CAs (CVE-2026-111943). ([#39417](https://github.com/hashicorp/terraform/pull/39417))

OTHER:

* Added a regression test for failed assertions on deprecated values, and renamed the internal test-output formatting helpers to make clear they are specific to `terraform test`. ([#39410](https://github.com/hashicorp/terraform/pull/39410))
* Updated the Go version in `go.mod` files and prepared the repository for the 1.16.7 release.


# CANDIDATE B

## 1.16.7 (October 22, 2026)

### BUG FIXES

* `terraform test` no longer crashes when a failed assertion involves a value from a deprecated attribute. ([#39406](https://github.com/hashicorp/terraform/pull/39406), backported in [#39410](https://github.com/hashicorp/terraform/pull/39410))

### NOTES

* Terraform is now built with Go 1.26.10, which no longer trusts certificates issued through a set of compromised eMudhra intermediate CAs (CVE-2026-111943). ([#39417](https://github.com/hashicorp/terraform/pull/39417))

### OTHER

* Renamed internal test-diagnostic formatting helpers and added a test with a deprecated attribute to the test provider. ([#39410](https://github.com/hashicorp/terraform/pull/39410))
* Updated the Go version in the build files and module files, and prepared the release metadata and changelog.

