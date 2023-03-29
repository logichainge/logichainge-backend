from typing import List
import pytest
from app import schemas
from .database import client, session


def test_root(client):
    res = client.get("/")
    print(res.json().get('message'))
    assert res.json().get('message') == 'Welcome to Logichainge'
    assert res.status_code == 200


def test_orm(session):
    assert True
#
#
# @pytest.fixture()
# def goods_object():
#     goods = schemas.GoodsBase(
#         activity_id=1,
#         unit_type="unit_type123",
#         stackable=True,
#         quantity=1,
#         description="description",
#         loading_meters=1.23,
#         net_weight=1.23,
#         gross_weight=1.23,
#         dangerous_goods=True,
#         dg_class="dg_class",
#         dg_product_group="dg_product_group",
#         dg_un_code="dg_un_code",
#         dg_technical_name="dg_technical_name"
#     )
#     return goods
#
#
# def test_create_goods(client, goods_object):
#     # print(goods_object.dict())
#     res = client.post("/goods/", json={**goods_object.dict()})
#     # print(res.json())
#     goods = schemas.GoodsOut(**res.json())
#     assert goods.unit_type == "unit_type123"
#     assert res.status_code == 201
#
#
# def test_get_all_goods(client):
#     res = client.get("/goods/")
#     goods_all = res.json()
#     print(goods_all)
#     goods_first = schemas.GoodsOut(**goods_all[0])
#     assert len(goods_all) > 0
#     assert goods_first.id
#
