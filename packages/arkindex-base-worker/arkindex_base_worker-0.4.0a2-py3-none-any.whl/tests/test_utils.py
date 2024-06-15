from pathlib import Path

import pytest

from arkindex_worker.utils import (
    close_delete_file,
    extract_tar_zst_archive,
    parse_source_id,
)

FIXTURES = Path(__file__).absolute().parent / "data"
ARCHIVE = FIXTURES / "archive.tar.zst"


@pytest.mark.parametrize(
    ("source_id", "expected"),
    [
        (None, None),
        ("", None),
        (
            "cafecafe-cafe-cafe-cafe-cafecafecafe",
            "cafecafe-cafe-cafe-cafe-cafecafecafe",
        ),
        ("manual", False),
    ],
)
def test_parse_source_id(source_id, expected):
    assert parse_source_id(source_id) == expected


def test_extract_tar_zst_archive(tmp_path):
    destination = tmp_path / "destination"
    _, archive_path = extract_tar_zst_archive(ARCHIVE, destination)

    assert archive_path.is_file()
    assert archive_path.suffix == ".tar"
    assert sorted(list(destination.rglob("*"))) == [
        destination / "archive.tar.zst",
        destination / "cache",
        destination / "cache/tables.sqlite",
        destination / "line_transcriptions_small.json",
        destination / "mirrored_image.jpg",
        destination / "page_element.json",
        destination / "rotated_image.jpg",
        destination / "rotated_mirrored_image.jpg",
        destination / "test_image.jpg",
        destination / "tiled_image.jpg",
        destination / "ufcn_line_historical_worker_version.json",
    ]


def test_close_delete_file(tmp_path):
    destination = tmp_path / "destination"
    archive_fd, archive_path = extract_tar_zst_archive(ARCHIVE, destination)
    close_delete_file(archive_fd, archive_path)

    assert not archive_path.exists()
