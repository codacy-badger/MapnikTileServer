import pytest
from ohdm_django_mapnik.ohdm.import_osh import run_import as run_osh_import
from ohdm_django_mapnik.ohdm.import_osm import run_import as run_osm_import
from ohdm_django_mapnik.ohdm.models import (
    PlanetOsmLine,
    PlanetOsmPoint,
    PlanetOsmPolygon,
    PlanetOsmRoads,
)
from ohdm_django_mapnik.ohdm.rel2pgsql import Rel2pgsql


@pytest.mark.django_db()
def test_import_osm():
    # fill database with osm importer
    run_osm_import(
        file_path="/niue-latest.osm.pbf", db_cache_size=10000, cache2file=False,
    )

    # count mapnik entries
    osm_point_count: int = PlanetOsmPoint.objects.all().count()
    osm_line_count: int = PlanetOsmLine.objects.all().count()
    osm_road_count: int = PlanetOsmRoads.objects.all().count()
    osm_polygon_count: int = PlanetOsmPolygon.objects.all().count()

    # check if there was added any mapnik entry
    if osm_point_count <= 0:
        raise AssertionError
    if osm_line_count <= 0:
        raise AssertionError
    if osm_road_count <= 0:
        raise AssertionError
    if osm_polygon_count <= 0:
        raise AssertionError


@pytest.mark.django_db()
def test_import_osh():
    # fill database with osh importer
    run_osh_import(
        file_path="/niue-latest.osm.pbf", db_cache_size=10000, cache2file=False,
    )

    # convert relations to mapnik tables
    rel2pgsql: Rel2pgsql = Rel2pgsql(chunk_size=10000)
    rel2pgsql.run_import()

    # count mapnik entries
    osh_point_count: int = PlanetOsmPoint.objects.all().count()
    osh_line_count: int = PlanetOsmLine.objects.all().count()
    osh_road_count: int = PlanetOsmRoads.objects.all().count()
    osh_polygon_count: int = PlanetOsmPolygon.objects.all().count()

    # check if there was added any mapnik entry
    if osh_point_count <= 0:
        raise AssertionError
    if osh_line_count <= 0:
        raise AssertionError
    if osh_road_count <= 0:
        raise AssertionError
    if osh_polygon_count <= 0:
        raise AssertionError
