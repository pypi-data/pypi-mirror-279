from unittest import mock
import pytest

from signtractions.resources.signing_wrapper import (
    SignerWrapper,
    SignerWrapperSettings,
    SignEntry,
    MsgSignerWrapper,
    MsgSignerSettings,
    SigningError,
)


def test_signer_wrapper_run_entrypoint():
    sw = SignerWrapper(config_file="", settings=SignerWrapperSettings())
    m = mock.Mock()
    with mock.patch("pkg_resources.load_entry_point") as mock_load_entry_point:
        mock_load_entry_point.return_value = m
        assert sw.entry_point == m
        # property test
        assert sw.entry_point == m


def test_signer_wrapper_remove_signatures():
    with mock.patch(
        "signtractions.resources.signing_wrapper.SignerWrapper._run_remove_signatures"
    ) as mocked_run_remove_signatures:
        sw = SignerWrapper(config_file="", settings=SignerWrapperSettings())
        sw.remove_signatures("test")
        mocked_run_remove_signatures.assert_called_once_with("test")


def test_signer_wrapper_run_store_signed():
    with mock.patch(
        "signtractions.resources.signing_wrapper.SignerWrapper._run_store_signed"
    ) as mocked_run_store_signed:
        sw = SignerWrapper(config_file="", settings=SignerWrapperSettings())
        m = mock.Mock()
        sw._store_signed(m)
        mocked_run_store_signed.assert_called_once_with(m)


def test_signer_wrapper_sign_containers():
    sw = SignerWrapper(config_file="", settings=SignerWrapperSettings())
    with mock.patch("pkg_resources.load_entry_point") as mock_load_entry_point:
        ep = mock.Mock()
        mock_load_entry_point.return_value = ep
        ep.return_value = {"signer_result": {"status": "ok"}}
        sw.sign_containers(
            [
                SignEntry(
                    repo="containers/podman",
                    reference="quay.io/containers/podman:latest",
                    digest="sha256:123456",
                    arch="amd64",
                    signing_key="signing_key",
                )
            ]
        )
        ep.assert_called_with(
            config_file="",
            signing_key="signing_key",
            reference=["quay.io/containers/podman:latest"],
            digest=["sha256:123456"],
        )


def test_signer_wrapper_sign_containers_error():
    sw = SignerWrapper(config_file="", settings=SignerWrapperSettings())
    with mock.patch("pkg_resources.load_entry_point") as mock_load_entry_point:
        ep = mock.Mock()
        mock_load_entry_point.return_value = ep
        ep.return_value = {"signer_result": {"status": "error", "error_message": "test_message"}}
        with pytest.raises(SigningError):
            sw.sign_containers(
                [
                    SignEntry(
                        repo="containers/podman",
                        reference="quay.io/containers/podman:latest",
                        digest="sha256:123456",
                        arch="amd64",
                        signing_key="signing_key",
                    )
                ]
            )


def test_signer_wrapper_sign_containers_nothing_to_sign():
    sw = SignerWrapper(config_file="", settings=SignerWrapperSettings())
    with mock.patch("pkg_resources.load_entry_point") as mock_load_entry_point:
        ep = mock.Mock()
        mock_load_entry_point.return_value = ep
        ep.return_value = {"signer_result": {"status": "ok"}}
        sw.sign_containers([])
        ep.assert_not_called()


def test_msg_signer_wrapper_sign_containers():
    sw = MsgSignerWrapper(
        config_file="",
        settings=MsgSignerSettings(pyxis_server="", pyxis_ssl_crt_file="", pyxis_ssl_key_file=""),
    )

    with mock.patch("pkg_resources.load_entry_point") as mock_load_entry_point:
        ep = mock.Mock()
        mock_load_entry_point.return_value = ep
        ep.return_value = {"signer_result": {"status": "ok"}}
        sw.sign_containers(
            [
                SignEntry(
                    repo="containers/podman",
                    reference="quay.io/containers/podman:latest",
                    digest="sha256:123456",
                    arch="amd64",
                    signing_key="signing_key",
                )
            ]
        )
        ep.assert_called_with(
            config_file="",
            signing_key="signing_key",
            reference=["quay.io/containers/podman:latest"],
            digest=["sha256:123456"],
        )


def test_msg_signer_wrapper_filter_to_sign():
    msw = MsgSignerWrapper(
        config_file="",
        settings=MsgSignerSettings(pyxis_server="", pyxis_ssl_crt_file="", pyxis_ssl_key_file=""),
    )
    with mock.patch(
        "signtractions.resources.signing_wrapper.MsgSignerWrapper._fetch_signatures"
    ) as mocked_fetch_signatures:
        mocked_fetch_signatures.return_value = []
        assert msw._filter_to_sign(
            [
                SignEntry(
                    repo="containers/podman",
                    reference="quay.io/containers/podman:latest",
                    digest="sha256:123456",
                    arch="amd64",
                    signing_key="signing_key",
                )
            ]
        ) == [
            SignEntry(
                repo="containers/podman",
                reference="quay.io/containers/podman:latest",
                digest="sha256:123456",
                arch="amd64",
                signing_key="signing_key",
            )
        ]


def test_msg_signer_wrapper_store_signed():
    sw = MsgSignerWrapper(
        config_file="",
        settings=MsgSignerSettings(pyxis_server="", pyxis_ssl_crt_file="", pyxis_ssl_key_file=""),
    )
    with mock.patch(
        "signtractions.resources.signing_wrapper.run_entrypoint_mod"
    ) as mock_run_entrypoint_mod:
        sw._store_signed(
            {
                "operation": {"references": ["registry.com/namespace/repo:latest"]},
                "signing_key": "signing_key",
                "operation_results": [
                    (
                        {
                            "msg": {
                                "repo": "repository",
                                "signed_claim": "signed_claim",
                                "manifest_digest": "digest",
                            },
                            "status": "ok",
                        },
                        True,
                    )
                ],
            }
        )
        mock_run_entrypoint_mod.assert_called_with(
            ("pubtools-pyxis", "console_scripts", "pubtools-pyxis-upload-signatures"),
            "pubtools-pyxis-upload-signature",
            [
                "--pyxis-server",
                "",
                "--pyxis-ssl-crtfile",
                "",
                "--pyxis-ssl-keyfile",
                "",
                "--request-threads",
                "7",
                "--signatures",
                mock.ANY,
            ],
            {},
        )


def test_msg_signer_wrapper_filter_to_sign_nothing_to_sign():
    msw = MsgSignerWrapper(
        config_file="",
        settings=MsgSignerSettings(pyxis_server="", pyxis_ssl_crt_file="", pyxis_ssl_key_file=""),
    )
    with mock.patch(
        "signtractions.resources.signing_wrapper.MsgSignerWrapper._fetch_signatures"
    ) as mocked_fetch_signatures:
        mocked_fetch_signatures.return_value = [
            {
                "repo": "containers/podman",
                "reference": "quay.io/containers/podman:latest",
                "manifest_digest": "sha256:123456",
                "arch": "amd64",
                "sig_key_id": "signing_key",
            }
        ]
        assert (
            msw._filter_to_sign(
                [
                    SignEntry(
                        repo="containers/podman",
                        reference="quay.io/containers/podman:latest",
                        digest="sha256:123456",
                        arch="amd64",
                        signing_key="signing_key",
                    )
                ]
            )
            == []
        )


def test_msg_signer_fetch_signature():
    with mock.patch(
        "signtractions.resources.signing_wrapper.run_entrypoint"
    ) as mocked_run_entrypoint:
        mocked_run_entrypoint.return_value = ["digest-1"]
        msw = MsgSignerWrapper(
            config_file="",
            settings=MsgSignerSettings(
                pyxis_server="", pyxis_ssl_crt_file="", pyxis_ssl_key_file=""
            ),
        )
        next(msw._fetch_signatures(["digest"]))
        mocked_run_entrypoint.assert_called_once_with(
            ("pubtools-pyxis", "console_scripts", "pubtools-pyxis-get-signatures"),
            "pubtools-pyxis-get-signatures",
            [
                "--pyxis-server",
                "",
                "--pyxis-ssl-crtfile",
                "",
                "--pyxis-ssl-keyfile",
                "",
                "--manifest-digest",
                mock.ANY,
            ],
            {},
        )


def test_msg_signer_remove_signature():
    with mock.patch(
        "signtractions.resources.signing_wrapper.run_entrypoint"
    ) as mocked_run_entrypoint:
        mocked_run_entrypoint.return_value = [
            {
                "manifest_digest": "digest",
                "reference": "registry.com/namespace/repo:latest",
                "repository": "repository",
                "_id": "id1",
                "sig_key_id": "signing_key",
            }
        ]
        msw = MsgSignerWrapper(
            config_file="",
            settings=MsgSignerSettings(
                pyxis_server="", pyxis_ssl_crt_file="", pyxis_ssl_key_file=""
            ),
        )
        msw.remove_signatures([("digest", "latest", "repository")])
        mocked_run_entrypoint.assert_has_calls(
            [
                mock.call(
                    ("pubtools-pyxis", "console_scripts", "pubtools-pyxis-get-signatures"),
                    "pubtools-pyxis-get-signatures",
                    [
                        "--pyxis-server",
                        "",
                        "--pyxis-ssl-crtfile",
                        "",
                        "--pyxis-ssl-keyfile",
                        "",
                        "--manifest-digest",
                        mock.ANY,
                    ],
                    {},
                )
            ]
        )
