import pytest
from httpx import AsyncClient

from src.category.scemas import CategoryBase
from tests.response import MyResponse


@pytest.mark.parametrize('url, request_type', [
    ('/categories', 'get'),
    ('/categories/1', 'get'),
    ('/categories', 'post'),
    ('/categories/1', 'put'),
    ('/categories/1', 'delete'),
])
async def test_categories_without_access(unauthorized_client: AsyncClient,
                                         url: str, request_type: str):
    request = getattr(unauthorized_client, request_type)
    r = await request(url=url)
    MyResponse(r).assert_status_code(401).assert_json({"detail": "Unauthorized"})


async def test_get_empty_categories(authorized_client_1: AsyncClient):
    r = await authorized_client_1.get(url='/categories')
    MyResponse(r).assert_status_code(200).assert_json([])


@pytest.mark.parametrize('name', ['Cat1', 'Cat2'])
async def test_create_category(authorized_client_1: AsyncClient, name: str):
    r = await authorized_client_1.post(url='/categories',
                                       json={'name': name})
    MyResponse(r).assert_status_code(201).validate(schema=CategoryBase)


async def test_create_category_with_existing_name(authorized_client_1: AsyncClient):
    r = await authorized_client_1.post(url='/categories',
                                       json={'name': 'Cat1'})
    MyResponse(r).assert_status_code(400).assert_json({"detail": "Category with this name already exists"})


async def test_get_category(authorized_client_1: AsyncClient):
    r = await authorized_client_1.get(url='/categories/1')
    MyResponse(r).assert_status_code(200).validate(schema=CategoryBase)


async def test_get_category_another_owner(authorized_client_2: AsyncClient):
    r = await authorized_client_2.get(url='/categories/1')
    MyResponse(r).assert_status_code(403).assert_json({"detail": "Access denied"})


async def test_get_category_not_found(authorized_client_1: AsyncClient):
    r = await authorized_client_1.get(url='/categories/3')
    MyResponse(r).assert_status_code(404).assert_json({"detail": "Category not found"})


async def test_get_list_categories(authorized_client_1: AsyncClient):
    r = await authorized_client_1.get(url='/categories')
    MyResponse(r).assert_status_code(200).assert_len(2).validate(schema=CategoryBase)


async def test_update_category(authorized_client_1: AsyncClient):
    r = await authorized_client_1.put(url='/categories/1',
                                      json={'name': 'Cat3'})
    MyResponse(r).assert_status_code(200).validate(schema=CategoryBase)


async def test_update_category_another_owner(authorized_client_2: AsyncClient):
    r = await authorized_client_2.put(url='/categories/1',
                                      json={'name': 'Cat3'})
    MyResponse(r).assert_status_code(403).assert_json({"detail": "Access denied"})


async def test_update_category_not_found(authorized_client_1: AsyncClient):
    r = await authorized_client_1.get(url='/categories/3')
    MyResponse(r).assert_status_code(404).assert_json({"detail": "Category not found"})


async def test_delete_category(authorized_client_1: AsyncClient):
    r = await authorized_client_1.delete(url='/categories/2')
    MyResponse(r).assert_status_code(200).validate(schema=CategoryBase)


async def test_delete_category_another_owner(authorized_client_2: AsyncClient):
    r = await authorized_client_2.delete(url='/categories/1')
    MyResponse(r).assert_status_code(403).assert_json({"detail": "Access denied"})


async def test_delete_category_not_found(authorized_client_1: AsyncClient):
    r = await authorized_client_1.delete(url='/categories/2')
    MyResponse(r).assert_status_code(404).assert_json({"detail": "Category not found"})
