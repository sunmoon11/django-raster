from __future__ import unicode_literals

from django.test.utils import override_settings
from raster.const import PK_FORMAT
from raster.models import RasterTile

from .raster_testcase import RasterTestCase


@override_settings(RASTER_TILE_CACHE_TIMEOUT=0)
class VerbosePkTests(RasterTestCase):

    def test_pk_construction_on_save(self):
        tile = RasterTile.objects.first()
        self.assertEqual(tile.pk, PK_FORMAT.format(
            layer=tile.rasterlayer_id, tilez=tile.tilez, tilex=tile.tilex, tiley=tile.tiley
        ))
        tile.pk = None
        tile.tilez = 18
        tile.save()
        self.assertEqual(tile.pk, PK_FORMAT.format(
            layer=tile.rasterlayer_id, tilez=18, tilex=tile.tilex, tiley=tile.tiley
        ))

    def test_pk_filter(self):
        tile = RasterTile.objects.first()
        qs = RasterTile.objects.filter_by_pk(
            rasterlayer_id=tile.rasterlayer_id,
            tilez=tile.tilez,
            tilex=tile.tilex,
            tiley=tile.tiley,
        ).only('id')
        self.assertEqual(
            qs.query.__str__(),
            'SELECT "raster_rastertile"."id" FROM "raster_rastertile" WHERE "raster_rastertile"."id" = ' + tile.pk,
        )

    def test_pk_get(self):
        tile = RasterTile.objects.first()
        tile_by_pk = RasterTile.objects.get_by_pk(
            rasterlayer_id=tile.rasterlayer_id,
            tilez=tile.tilez,
            tilex=tile.tilex,
            tiley=tile.tiley,
        )
        self.assertEqual(tile, tile_by_pk)
