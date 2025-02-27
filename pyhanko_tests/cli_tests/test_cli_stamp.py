from pyhanko.cli import cli_root
from pyhanko_tests.cli_tests.conftest import (
    INPUT_PATH,
    SIGNED_OUTPUT_PATH,
    _write_config,
)


def test_cli_stamp_with_style(cli_runner):
    cfg = {
        'stamp-styles': {'test': {'type': 'text', 'background': '__stamp__'}}
    }
    _write_config(cfg)
    result = cli_runner.invoke(
        cli_root,
        [
            'stamp',
            '--style-name',
            'test',
            INPUT_PATH,
            SIGNED_OUTPUT_PATH,
            '0',
            '0',
        ],
    )
    assert not result.exception, result.output
    # TODO make this a layout test


def test_cli_stamp_with_qr_style(cli_runner):
    cfg = {'stamp-styles': {'test': {'type': 'qr', 'background': '__stamp__'}}}
    _write_config(cfg)
    result = cli_runner.invoke(
        cli_root,
        [
            'stamp',
            '--style-name',
            'test',
            INPUT_PATH,
            SIGNED_OUTPUT_PATH,
            '0',
            '0',
            '--stamp-url',
            'https://example.com',
        ],
    )
    assert not result.exception, result.output
    # TODO make this a layout test


def test_cli_stamp_style_no_config(cli_runner):
    result = cli_runner.invoke(
        cli_root,
        [
            'stamp',
            '--style-name',
            'test',
            INPUT_PATH,
            SIGNED_OUTPUT_PATH,
            '0',
            '0',
        ],
    )
    assert result.exit_code == 1
    assert "requires a configuration file" in result.output


def test_cli_stamp_style_stamp_url_unnecessary(cli_runner):
    cfg = {
        'stamp-styles': {'test': {'type': 'text', 'background': '__stamp__'}}
    }
    _write_config(cfg)
    result = cli_runner.invoke(
        cli_root,
        [
            'stamp',
            '--style-name',
            'test',
            INPUT_PATH,
            SIGNED_OUTPUT_PATH,
            '0',
            '0',
            '--stamp-url',
            'blah',
        ],
    )
    assert result.exit_code == 1
    assert "only meaningful for QR" in result.output


def test_cli_stamp_style_stamp_url_mandatory(cli_runner):
    cfg = {'stamp-styles': {'test': {'type': 'qr', 'background': '__stamp__'}}}
    _write_config(cfg)
    result = cli_runner.invoke(
        cli_root,
        [
            'stamp',
            '--style-name',
            'test',
            INPUT_PATH,
            SIGNED_OUTPUT_PATH,
            '0',
            '0',
        ],
    )
    assert result.exit_code == 1
    assert "require the --stamp-url option" in result.output


def test_cli_stamp_style_undefined(cli_runner):
    cfg = {
        'stamp-styles': {'test': {'type': 'text', 'background': '__stamp__'}}
    }
    _write_config(cfg)
    result = cli_runner.invoke(
        cli_root,
        [
            'stamp',
            '--style-name',
            'undefined',
            INPUT_PATH,
            SIGNED_OUTPUT_PATH,
            '0',
            '0',
        ],
    )
    assert result.exit_code == 1
    assert "is properly defined" in result.output
